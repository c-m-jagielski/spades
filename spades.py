# Spades game
from deck import deck
import random

class spades(object):

    playerName = ""
    numPlayers = 4
    d = None
    playerCards = {}
    playerBids = {"p1":None, "p2":None, "p3":None, "p4":None}

    def startGame(self):
        """
        """
        # Start the game by dealing
        d = deck()
        playerCards = deck.deal(d, numPlayers=4, debug=True)

        # Show the user their hand
        self.displayHand(playerCards["p1"])

        # Assume the user is going to bid first
        p1bid = raw_input("\nWhat is your bid? ")
        #TODO error checking for integer between 0 and 13
        #TODO allow "null", "nello", and variations too

        # Obtain bids from the CPU users
        p2bid = self.obtainCpuBid(playerCards["p2"])
        p3bid = self.obtainCpuBid(playerCards["p3"])
        p4bid = self.obtainCpuBid(playerCards["p4"])

        print "You bid ", p1bid
        print "P 2 bid ", p2bid
        print "P 3 bid ", p3bid
        print "P 4 bid ", p4bid

        # User can play first
        self.displayHand(playerCards["p1"])
        cardSelection = raw_input("**** **** **** ****\nWhat card will you play? ")

    def reset(self):
        """
        Reset variables in this class
        """
        d = None
        playerCards = {}

    def displayHand(self, inputCards):
        """
        Sort then print user's cards
        """
        # TODO
        myCards = self.sortHand(inputCards)
        print "\n\n**** **** **** ****"
        #print myCards
        i = 0
        while i < len(myCards):
            print i+1, ")\t", myCards[i]["value"], "\t", myCards[i]["suit"]
            i += 1

    def sortHand(self, hand):
        """
        Sort the player's hand according to the json index
        """
        # TODO I can make this better
        sortedHand = []
        tmp = hand
        for i in range(1, 53):
            if len(tmp) == 0: break
            print "$$ i=", i
            handIndex = 0
            for ii in range(0, len(tmp)):
                thisCard = tmp[ii]
                print "$$   thisCard=", thisCard
                if thisCard["index"] == i:
                    blah = tmp.pop(handIndex)
                    print "$$      blah", blah
                    sortedHand.append(blah)
                    break
                handIndex += 1
        print "$$    sortedHand", sortedHand
        return sortedHand

    def obtainCpuBid(self, hand):
        # TODO
        return random.randint(1,4)

if __name__ == "__main__":
    print("Let's play Spades!")
    #val = raw_input("Enter your value: ")    # convert to input() for python 3.6
    playerName = raw_input("What is your name? ")
    if playerName=="": playerName = "Player 1"

    game = spades()
    game.startGame()