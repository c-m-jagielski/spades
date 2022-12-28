# python code for a deck of cards

import json
import random

class deck(object):

    size = 52
    S = "spades"
    C = "clubs"
    D = "diamonds"
    H = "hearts"
    suits = [S, C, D, H]

    def shuffle(self, cards=None):
        """
        Shuffle the cards so that the imported deck is now in a random order
        """
        if cards==None: return None

        i = 0
        tmp = cards
        new = []
        while i < self.size:
            x1 = random.randint(0, len(tmp)-1)
            #print x1
            new.append(tmp[x1])
            tmp.pop(x1)
            i += 1
        #print new
        #print tmp
        #print len(new)

    def deal(self, numPlayers=4):
        """
        Deal the cards. Default to 4 players.
        """
        f = open('cards.json')
        data = json.load(f)
        #print data

        player1 = []
        player2 = []
        player3 = []
        player4 = []

        newCards = self.shuffle(data)


if __name__ == "__main__":
    print("init")
    f = open('cards.json')
    data = json.load(f)
    #print data

    d = deck()
    d.deal()