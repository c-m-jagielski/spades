# Spades game
from deck import deck
import random, copy, time

class spades(object):

    playerName = ""
    numPlayers = 4
    d = None
    playerCards = {}
    playerBids = {"p1":None, "p2":None, "p3":None, "p4":None}
    spadesUsed = False

    # Modes for playing
    EASY = 1
    HARD = 2
    gameMode = EASY

    teamPoints = {"team1":0, "team2":0}

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

        roundCards = {}

        # User can play first
        self.displayHand(playerCards["p1"])
        usersHand = self.sortHand(playerCards["p1"])
        cardSelection = int(raw_input("\n\nWhat card will you play? ")) - 1

        # Is the user's selection allowed?
        isAllowed = self.checkLeadCard(usersHand, cardSelection)
        if not isAllowed:
            self.prepareResponse()
            print "\n\nYou can not select a SPADE yet. Try again."
            cardSelection = int(raw_input("\n\nWhat card will you play? ")) - 1

        usersHand.pop(cardSelection)

        roundCards["p1"] = usersHand[cardSelection]
        roundCards["p2"] = None
        roundCards["p3"] = None
        roundCards["p4"] = None

        leadSuit = roundCards["p1"]["suit"]
        leadPlayer = "p1"

        # Time for CPU's to play
        roundCards["p2"] = self.selectCPUCard(playerCards["p2"], roundCards, leadSuit, leadPlayer)
        roundCards["p3"] = self.selectCPUCard(playerCards["p3"], roundCards, leadSuit, leadPlayer)
        roundCards["p4"] = self.selectCPUCard(playerCards["p4"], roundCards, leadSuit, leadPlayer)

        # Find out who wins this round, they will go first next round
        winner = self.selectRoundWinner(roundCards, leadSuit)

    def selectCPUCard(self, hand, roundCards, leadSuit, leadPlayer):
        """
        CPU will select a valid card to play.
        This function is not for when a CPU user is the lead initiating a round.

        If CPU user has same suit as lead suit, must play that.
        If CPU user does not have same suit as lead suit, can play anything.

        hand: [input] the current user's full hand of cards
        roundCards: [input] dict of current cards already played this round
        leadSuit: [input] suit that was lead this round
        leadPlayer: [input] player that lead this round
        """
        selection = None

        print "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        print "CPU hand: \t", hand
        print "Lead suit: \t", leadSuit
        print "Round cards: \t", roundCards
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"

        # User must play the suited card if they have it
        ableToPlay = []
        for i in range(0, len(hand)):
            if hand[i]["suit"] == leadSuit: ableToPlay.append(hand[i])

        if len(ableToPlay) < 1:
            ableToPlay = copy.deepcopy(hand)
        print "ableToPlay: ", ableToPlay

        i = None
        if self.gameMode == self.HARD:
            #TODO purposefully choose which card to play
            i = 0 #Hardcode so this doesn't break
            pass
        else:
            # Choose a random card
            i = random.randint(0,len(ableToPlay)-1)

        selection = ableToPlay[i]
        hand.pop(i)
        print "selection: ", selection
        return selection

    def selectRoundWinner(self, roundCards, leadSuit):
        """
        Determine which player wins this round and obtains a trick.
        """
        return None

    def checkLeadCard(self, hand, cardSelection):
        """
        Check if a card played is allowed or not.
        Spades can't be lead unless already played or if user has no other choice.

        hand: [input] the user's hand, json format
        cardSelection: [input] integer selection, index starts at Zero
        """
        #print "^ INDEX: ", cardSelection
        #print "^ CARD: ", hand[cardSelection]

        if self.spadesUsed or hand[cardSelection]['suit'] != 'spades': return True

        # Check if user has only spades left
        i = 0
        while i < len(hand):
            if hand[i]['suit'] != 'spades': return False
            i += 1
        return True

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

    def obtainCpuBid(self, hand, mode=None):
        """
        Algorithm to determine the bid of a CPU player
        """

        # Easy or Hard mode will determine the algorithm/logic to use
        if mode == None: mode = self.EASY

        if mode == self.EASY: return random.randint(1,4)

        # TODO Hard mode

    def obtainUserBid(self):
        """
        User submits their bid. Check that it's legit.
        """
        allowed = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13",'null','nill','nillo','zero','none']
        response = raw_input("\nWhat is your bid? ")
        if response in allowed: return response
        self.prepareResponse()
        newResponse = raw_input("\nPlease enter a valid bid.\nWhat is your bid? ")
        if newResponse in allowed: return newResponse
        time.sleep(0.1)
        print "\n........."
        time.sleep(0.1)
        print "Sorry. Defaulting to a bid of 2."
        return 2

    def prepareResponse(self):
        """
        Prepare to give the user a response
        """
        time.sleep(0.1)
        print "\n........."
        time.sleep(0.1)

if __name__ == "__main__":
    print("Let's play Spades!")
    #val = raw_input("Enter your value: ")    # convert to input() for python 3.6
    playerName = raw_input("What is your name? ")
    if playerName=="": playerName = "Player 1"

    game = spades()
    game.startGame()