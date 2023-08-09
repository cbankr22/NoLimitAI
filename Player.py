class Player:
    def __init__(self, starting_stack, number, position):
        self.starting_stack = starting_stack
        self.stack = starting_stack
        self.number = "Player" + str(number)
        self.cards = (0, 0)
        self.position = position
        self.cancheck = position
        self.cancall = (position + 1) % 2
    def __str__(self):
        return self.number + ", " + str(self.stack)

    def reset(self, position):
        self.stack = self.starting_stack
        self.cards = (0, 0)
        self.position = position
        self.cancheck = position
        self.cancall = (position + 1) % 2

