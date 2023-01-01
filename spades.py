# Spades game
from deck import deck
import random, copy, time

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
        playerCards = deck.deal(d, numPlayers=4, debug=False)

        # Show the user their hand
        self.displayHand(playerCards["p1"])

        # Assume the user is going to bid first
        p1bid = self.obtainUserBid()

        # Obtain bids from the CPU users
        p2bid = self.obtainCpuBid(playerCards["p2"])
        p3bid = self.obtainCpuBid(playerCards["p3"])
        p4bid = self.obtainCpuBid(playerCards["p4"])

        print " "
        time.sleep(.5)
        print "You bid: ", p1bid
        print "P 2 bid: ", p2bid
        print "P 3 bid: ", p3bid
        print "P 4 bid: ", p4bid
        time.sleep(.5)

        # User can play first
        self.displayHand(playerCards["p1"])
        cardSelection = raw_input("\n\nWhat card will you play? ")

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
        myCards = self.sortHand(inputCards)
        print "\n\n**** **** **** **** **** **** ****"
        print "          YOUR HAND\n**** **** **** **** **** **** ****"

        i = 0
        while i < len(myCards):
            print i+1, ")\t", myCards[i]["value"], "\t", myCards[i]["suit"]
            i += 1
        print " "

    def sortHand(self, hand):
        """
        Sort the player's hand according to the json index
        """
        # TODO I can make this better
        sortedHand = []
        tmp = copy.deepcopy(hand)
        for i in range(1, 53):
            if len(tmp) == 0: break
            #print "$$ i=", i
            handIndex = 0

            for ii in range(0, len(tmp)):
                thisCard = tmp[ii]
                #print "$$   thisCard=", thisCard
                if thisCard["index"] == i:
                    blah = tmp.pop(handIndex)
                    #print "$$      blah", blah
                    sortedHand.append(blah)
                    break
                handIndex += 1
        #print "$$    sortedHand", sortedHand  # Debug
        return sortedHand

    def obtainCpuBid(self, hand):
        # TODO
        return random.randint(1,4)

    def obtainUserBid(self):
        """
        User submits their bid. Check that it's legit.
        """
        allowed = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13",'null','nill','nillo','zero','none']
        response = raw_input("\nWhat is your bid? ")
        if response in allowed: return response
        time.sleep(0.1)
        print "\n........."
        time.sleep(0.1)
        newResponse = raw_input("\nPlease enter a valid bid.\nWhat is your bid? ")
        if newResponse in allowed: return newResponse
        time.sleep(0.1)
        print "\n........."
        time.sleep(0.1)
        print "Sorry. Defaulting to a bid of 2."
        return 2

if __name__ == "__main__":
    print("Let's play Spades!")
    #val = raw_input("Enter your value: ")    # convert to input() for python 3.6
    playerName = raw_input("What is your name? ")
    if playerName=="": playerName = "Player 1"

    game = spades()
    game.startGame()