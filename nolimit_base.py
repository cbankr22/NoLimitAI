import numpy as np
from gymnasium import spaces
import Deck
from Player import Player

class NoLimitBaseEnv():
    def __init__(self):
        self.agents = ["p1", "p2"]
        self.num_agents = len(self.agents)
        self.possible_agents = self.agents[:]
        self.control_rewards = [0 for _ in range(self.num_agents)]
        self.last_dones = [False for _ in range(self.num_agents)]
        self.last_obs = [None for _ in range(self.num_agents)]
        self.last_rewards = [np.float64(0) for _ in range(self.num_agents)]
        self.state_size = 8

        self.starting_stack = 100.0
        self.get_spaces()
        self.deck = Deck.Deck()
        self.players = [Player(100, (i + 1) % 2, (i + 1) % 2) for i in range(self.num_agents)]
        self.previous_pot = 0.0
        self.pot = 0.0
        self.small_blind = 1.0
        self.big_blind = 2.0
        self.first = True

    def get_spaces(self):
        # obsevation_space = [holecard1, holecard2, herochipcount, villainchipcount, potsize, position, cancheck, cancall]
        self.observation_space = [spaces.Box(0, 1, shape=(self.state_size,), dtype=np.float32) for _ in range(self.num_agents)]
        # action_space = Discrete(4) where 0 = fold, 1 = check, 2 = call, 3 = bet 1/3 pot
        self.action_space = [spaces.Discrete(4) for _ in range(self.num_agents)]

    def start(self):
        self.pot = self.small_blind + self.big_blind
        if self.players[0].position == 1:
            self.players[0].stack -= self.big_blind
            self.players[1].stack -= self.small_blind
        else:
            self.players[0].stack -= self.small_blind
            self.players[1].stack -= self.big_blind


    def deal(self):
        winner = self.deck.compare_hands(self.players[0].cards, self.players[1].cards)
        if winner == 1:
            self.control_rewards[0] = self.pot / 2.0
            self.control_rewards[1] = -self.pot / 2.0
        elif winner == 2:
            self.control_rewards[0] = -self.pot / 2.0
            self.control_rewards[1] = self.pot / 2.0
        else:
            self.control_rewards[0] = 0.0
            self.control_rewards[1] = 0.0
        self.last_dones = [True for _ in range(self.num_agents)]

    # sb action == 1, bb action == 1
    def step(self, action, agent_id, is_last):
        if action == 0:
            self.control_rewards[agent_id] = -self.pot / 2.0
            self.control_rewards[(agent_id + 1) % 2] = self.pot / 2.0
            self.last_dones = [True for _ in range(self.num_agents)]
        elif action == 1:
            if self.players[agent_id].cancheck == 1:
                self.deal()

            else:
                self.control_rewards[agent_id] = -self.pot / 2.0
                self.control_rewards[(agent_id + 1) % 2] = self.pot / 2.0
                self.last_dones = [True for _ in range(self.num_agents)]
        elif action == 2:
            if self.players[agent_id].cancall == 1:
                if self.first:
                    self.pot += self.small_blind
                    self.players[agent_id].stack -= self.small_blind
                    self.first = False
                else:
                    self.pot += (self.pot - self.previous_pot)
                    self.players[agent_id].stack -= (self.pot - self.previous_pot)
                    self.deal()
            else:
                self.control_rewards[agent_id] = -self.pot / 2.0
                self.control_rewards[(agent_id + 1) % 2] = self.pot / 2.0
                self.last_dones = [True for _ in range(self.num_agents)]
        elif action == 3:
            self.previous_pot = self.pot
            self.pot += int((1/3) * self.pot)
            self.players[agent_id].stack -= int((1/3) * self.pot)
            self.players[agent_id].cancall = 0
            self.players[(agent_id + 1) % 2].cancall = 1

    def reset(self):
        self.deck.reset()
        for player in self.players:
            player.reset((player.position + 1) % 2)
            player.cards = (self.deck.get_card(), self.deck.get_card())
        self.pot = 0.0
        self.first = True

        self.last_rewards = [np.float64(0) for _ in range(self.num_agents)]
        self.control_rewards = [0 for _ in range(self.num_agents)]
        self.last_dones = [False for _ in range(self.num_agents)]
        self.start()
        self.last_obs = self.observe_list()

        return self.last_obs[0]

    def observe(self, agent_id):
        return np.array(self.last_obs[agent_id], dtype=np.float32)

    def observe_list(self):
        observe_list = []

        for i, player in enumerate(self.players):
            state = np.zeros(self.state_size)
            state[0] = player.cards[0].id / 52.0
            state[1] = player.cards[1].id / 52.0
            state[2] = player.stack / self.starting_stack
            if i == 0:
                state[3] = self.players[1].stack / self.starting_stack
            else:
                state[3] = self.players[0].stack / self.starting_stack
            state[4] = self.pot / (2 * self.starting_stack)
            state[5] = player.position
            state[6] = player.cancheck
            state[7] = player.cancall
            observe_list.append(state)

        return observe_list


if __name__ == "__main__":
    env = NoLimitBaseEnv()
    env.reset()
    env.deal()
    #print(env.observe_list())
