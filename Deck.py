import random

class Deck:
    def __init__(self):
        self.num_cards = 52
        self.cards = []
        self.suites = ["hearts", "clubs", "diamonds", "spades"]
        self.new_deck()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def get_card(self):
        return self.cards.pop(0)

    def new_deck(self):
        for suite in self.suites:
            for i in range(13):
                self.cards.append(Card(suite, i+2))
        for i, card in enumerate(self.cards):
            card.id = i

    def compare_hands(self, hand1, hand2):
        print(hand1[0], hand1[1])
        print(hand2[0], hand2[1])
        onepair = False
        twopair = False
        if hand1[0].number == hand1[1].number:
            onepair = True
        if hand2[0].number == hand2[1].number:
            twopair = True
        if onepair and twopair:
            if hand1[0].number > hand2[0].number:
                return 1
            elif hand1[0].number < hand2[0].number:
                return 2
            else:
                return 0
        if onepair and not twopair:
            return 1
        if twopair and not onepair:
            return 2

        if hand1[0].number >= hand1[1].number:
            onehighest = hand1[0].number
            onelowest = hand1[1].number
        else:
            onehighest = hand1[1].number
            onelowest = hand1[0].number
        if hand2[0].number >= hand2[1].number:
            twohighest = hand2[0].number
            twolowest = hand2[1].number
        else:
            twohighest = hand2[1].number
            twolowest = hand2[0].number

        if onehighest > twohighest:
            return 1
        elif twohighest > onehighest:
            return 2
        else:
            if onelowest > twolowest:
                return 1
            elif twolowest > onelowest:
                return 2
            else:
                return 0

    def reset(self):
        self.cards = []
        self.new_deck()
        self.shuffle()


class Card:
    def __init__(self, suite, number):
        self.suite = suite
        self.id = 0
        self.number = number
        if number == 11:
            self.name = "J"
        elif number == 12:
            self.name = "Q"
        elif number == 13:
            self.name = "K"
        elif number == 14:
            self.name = "A"
        else:
            self.name = str(number)

    def __str__(self):
        return self.name + self.suite[0]

