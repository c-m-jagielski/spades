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

    def shuffle(self, cards=None, debug=False):
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
        if debug:
            print new
            print tmp
            print len(new)
        return new

    def deal(self, numPlayers=4, debug=False):
        """
        Deal the cards. Default to 4 players.
        """
        f = open('cards.json')
        data = json.load(f)
        if debug: print data

        player1 = []
        player2 = []
        player3 = []
        player4 = []

        newCards = self.shuffle(data)
        if debug: print newCards

        player1 = newCards[0:12]
        player2 = newCards[13:25]
        player3 = newCards[26:38]
        player4 = newCards[39:51]

        playerCards = {"p1":player1, "p2":player2, "p3":player3, "p4":player4}
        return playerCards

if __name__ == "__main__":
    print("init")
    f = open('cards.json')
    data = json.load(f)
    #print data

    d = deck()
    d.deal()