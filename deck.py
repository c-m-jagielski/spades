# python code for a deck of cards

import json

class deck(object):

    size = 52
    S = "spades"
    C = "clubs"
    D = "diamonds"
    H = "hearts"
    suits = [S, C, D, H]

    def deal(self, numPlayers=4):
        """
        Deal the cards. Default to 4 players.
        """

if __name__ == "__main__":
    print("init")
    f = open('cards.json')
    data = json.load(f)
    print data