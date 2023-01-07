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
    pointsToWin = 1  # 500

    def startGame(self):
        """
        Play a game until 1 team reaches 500 points.
        """

        # Use a count to determine which player will bid and lead first each round
        i = 0
        leaderSelection = {0:"p1", 1:"p2", 2:"p3", 3:"p4"}

        while not self.hasTeamWon():
            roundPoints = self.playRound(leadUser=leaderSelection[i%4])
            i += 1

            self.teamPoints["team1"] += roundPoints["team1"]
            self.teamPoints["team2"] += roundPoints["team2"]

    def playRound(self, leadUser="p1"):
        """
        Play a full round with the 4 players of 13 hands.
        """

        # Initialize who bids first & who leads first
        previousRoundWinner = copy.deepcopy(leadUser)

        # Start the round by dealing
        d = deck()
        unsortedCards = deck.deal(d, numPlayers=4, debug=False)

        # Sort each player's hand
        playerCards = {}
        playerCards["p1"] = self.sortHand(unsortedCards["p1"])
        playerCards["p2"] = self.sortHand(unsortedCards["p2"])
        playerCards["p3"] = self.sortHand(unsortedCards["p3"])
        playerCards["p4"] = self.sortHand(unsortedCards["p4"])

        # Get the bids from the 4 players, and ask them in order
        p1bid = None
        p2bid = None
        p3bid = None
        p4bid = None
        if leadUser == "p1":
            # Show the user their hand and get their bid first
            self.displayHand(playerCards["p1"])
            p1bid = self.obtainUserBid()

            # Now CPU's will bid
            p2bid = self.obtainCpuBid(playerCards["p2"])
            p3bid = self.obtainCpuBid(playerCards["p3"])
            p4bid = self.obtainCpuBid(playerCards["p4"])

        elif leadUser == "p2":
            p2bid = self.obtainCpuBid(playerCards["p2"])
            p3bid = self.obtainCpuBid(playerCards["p3"])
            p4bid = self.obtainCpuBid(playerCards["p4"])

            # Show the user their hand and get their bid
            print " "
            time.sleep(.5)
            print "P 2 bid: ", p2bid
            print "P 3 bid: ", p3bid
            print "P 4 bid: ", p4bid
            time.sleep(.5)

            self.displayHand(playerCards["p1"])
            p1bid = self.obtainUserBid()

        elif leadUser == "p3":
            p3bid = self.obtainCpuBid(playerCards["p3"])
            p4bid = self.obtainCpuBid(playerCards["p4"])

            # Show the user their hand and get their bid
            print " "
            time.sleep(.5)
            print "P 3 bid: ", p3bid
            print "P 4 bid: ", p4bid
            time.sleep(.5)
            self.displayHand(playerCards["p1"])
            p1bid = self.obtainUserBid()

            p2bid = self.obtainCpuBid(playerCards["p2"])

        elif leadUser == "p4":
            p4bid = self.obtainCpuBid(playerCards["p4"])

            # Show the user their hand and get their bid
            print " "
            time.sleep(.5)
            print "P 4 bid: ", p4bid
            time.sleep(.5)
            self.displayHand(playerCards["p1"])
            p1bid = self.obtainUserBid()

            p2bid = self.obtainCpuBid(playerCards["p2"])
            p3bid = self.obtainCpuBid(playerCards["p3"])
        else: pass

        # Display the bids to the user
        print " "
        time.sleep(.5)
        print "You bid: ", p1bid
        print "P 2 bid: ", p2bid
        print "P 3 bid: ", p3bid
        print "P 4 bid: ", p4bid
        time.sleep(.5)

        # Calculate team bids for this roundCards
        team1bid = p1bid + p3bid
        team2bid = p2bid + p4bid

        # A round has 13 hands to play in order to add up all the tricks
        trickTotals = {"p1":0, "p2":0, "p3":0, "p4":0}
        for r in range(1,14):
            winner = self.playHand(previousRoundWinner, playerCards)
            trickTotals[winner] += 1
            previousRoundWinner = copy.deepcopy(winner)

        # Calculate points for this round
        #TODO
        roundPoints = {"team1": 1, "team2": 2}
        return roundPoints

    def playHand(self, leadUser, playerCards):
        """
        Play a single hand, each player submits a card and somebody wins the trick.
        """
        roundCards = {}
        leadSuit = None

        if leadUser == "p1":
            roundCards["p1"] = self.userLeads(playerCards["p1"])
            leadSuit = roundCards[leadUser]["suit"]

            # Time for CPU's to play
            roundCards["p2"] = self.selectCPUCard(playerCards["p2"], roundCards, leadSuit, leadUser)
            roundCards["p3"] = self.selectCPUCard(playerCards["p3"], roundCards, leadSuit, leadUser)
            roundCards["p4"] = self.selectCPUCard(playerCards["p4"], roundCards, leadSuit, leadUser)

        if leadUser == "p2":
            roundCards["p2"] = self.selectCPULeadCard(playerCards["p2"])
            leadSuit = roundCards[leadUser]["suit"]

            roundCards["p3"] = self.selectCPUCard(playerCards["p3"], roundCards, leadSuit, leadUser)
            roundCards["p4"] = self.selectCPUCard(playerCards["p4"], roundCards, leadSuit, leadUser)
            roundCards["p1"] = self.userPlays(playerCards["p1"], leadSuit)

        if leadUser == "p3":
            roundCards["p3"] = self.selectCPULeadCard(playerCards["p3"])
            leadSuit = roundCards[leadUser]["suit"]

            roundCards["p4"] = self.selectCPUCard(playerCards["p4"], roundCards, leadSuit, leadUser)
            roundCards["p1"] = self.userPlays(playerCards["p1"], leadSuit)
            roundCards["p2"] = self.selectCPUCard(playerCards["p2"], roundCards, leadSuit, leadUser)

        if leadUser == "p4":
            roundCards["p4"] = self.selectCPULeadCard(playerCards["p4"])
            leadSuit = roundCards[leadUser]["suit"]

            roundCards["p1"] = self.userPlays(playerCards["p1"], leadSuit)
            roundCards["p2"] = self.selectCPUCard(playerCards["p2"], roundCards, leadSuit, leadUser)
            roundCards["p3"] = self.selectCPUCard(playerCards["p3"], roundCards, leadSuit, leadUser)

        # Find out who wins this hand, they get a trick & will go first next hand
        winner = self.selectRoundWinner(roundCards, leadSuit)
        return winner

    def userLeads(self, usersHand):
        """
        Human user leads this round and selects their first card out
        """
        self.displayHand(usersHand)
        print "\n\nYou have the lead this hand."
        cardSelection = int(raw_input("\n\nWhat card will you play? ")) - 1

        # Is the user's selection allowed?
        isAllowed = self.checkLeadCard(usersHand, cardSelection)
        if not isAllowed:
            self.prepareResponse()
            print "\n\nYou can not select a SPADE yet. Try again."
            cardSelection = int(raw_input("\n\nWhat card will you play? ")) - 1

        cardSelected = usersHand[cardSelection]
        usersHand.pop(cardSelection)
        return cardSelected

    def userPlays(self, usersHand, leadSuit):
        """
        Human user plays a card in this round. User is not leading the hand.
        """
        self.displayHand(usersHand)
        print "\n\nLead suit was", leadSuit
        cardSelection = int(raw_input("\n\nWhat card will you play? ")) - 1

        # Is the user's selection allowed?
        isAllowed = self.checkPlayedCard(usersHand, cardSelection, leadSuit)
        if not isAllowed:
            self.prepareResponse()
            print "\n\nYour selection is not allowed. Try again."
            cardSelection = int(raw_input("\n\nWhat card will you play? ")) - 1

        cardSelected = usersHand[cardSelection]
        usersHand.pop(cardSelection)
        return cardSelected

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

        """
        print "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        print "CPU hand: \t", hand
        print "Lead suit: \t", leadSuit
        print "Round cards: \t", roundCards
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
        """

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

    def selectCPULeadCard(self, hand):
        """
        Select the lead card the CPU player will play for a given hand.

        In EASY mode, make it random.
        In HARD mode, purposefully choose which card to lead with.
        """

        ableToPlay = []

        if self.spadesUsed:
            # Can lead with anything
            ableToPlay = copy.deepcopy(hand)
        else:
            for i in range(0, len(hand)):
                if hand[i]["suit"] != 'spades': ableToPlay.append(hand[i])

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
        Determine which player wins this round and obtains a hand.
        """
        print "\n\n\n"
        print "\tleadSuit: ", leadSuit
        print "\troundCards: ", roundCards

        # If someone played a spade, the highest spade wins
        suits = [roundCards["p1"]["suit"], roundCards["p2"]["suit"],
            roundCards["p3"]["suit"], roundCards["p4"]["suit"]]

        winningSuit = leadSuit

        # Check for spades & toggle the global spade var, too
        if 'spades' in suits:
            winningSuit = 'spades'
            self.spadesUsed = True

        # Pick the winner; start with first eligible player then see if anyone beats them
        winner = None
        eligibleCards = []
        if roundCards["p1"]["suit"] == winningSuit: eligibleCards.append(roundCards["p1"])
        if roundCards["p2"]["suit"] == winningSuit: eligibleCards.append(roundCards["p2"])
        if roundCards["p3"]["suit"] == winningSuit: eligibleCards.append(roundCards["p3"])
        if roundCards["p4"]["suit"] == winningSuit: eligibleCards.append(roundCards["p4"])
        winner = eligibleCards[0]
        print "###\twinner: ", winner
        for i in range(1, len(eligibleCards)):
            if eligibleCards[i]["index"] > winner["index"]: winner = eligibleCards[i]
            print "###\twinner: ", winner

        # Find the user that won the hand
        winningUser = None
        for i in ["p1", "p2", "p3", "p4"]:
            if roundCards[i] == winner:
                winningUser = i
                break
        print "winningUser: ", winningUser
        return winningUser

    def checkLeadCard(self, hand, cardSelection):
        """
        Check if a lead card played is allowed or not.
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

    def checkPlayedCard(self, hand, cardSelection, leadSuit):
        """
        Check if a card played is allowed or not.
        Off-suit can't be played in response to a hand unless the lead was spades or the
         user has no cards of the lead suit.
        """
        if hand[cardSelection]['suit'] == leadSuit: return True

        i = 0
        while i < len(hand):
            if hand[i]['suit'] == leadSuit: return False
            i += 1

        # At this point we know the user's card played is off-suit & anything is allowed.
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
        myCards = inputCards #self.sortHand(inputCards)
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
        nillos = ['null','nill','nillo','zero','none']

        response = raw_input("\nWhat is your bid? ")
        if response in allowed:
            if response in nillos: return 0
            return int(response)

        self.prepareResponse()
        newResponse = raw_input("\nPlease enter a valid bid.\nWhat is your bid? ")
        if newResponse in allowed:
            if newResponse in nillos: return 0
            return int(newResponse)

        self.prepareResponse()
        print "Sorry. Defaulting to a bid of 2."
        return 2

    def prepareResponse(self):
        """
        Prepare to give the user a response
        """
        time.sleep(0.1)
        print "\n........."
        time.sleep(0.1)

    def hasTeamWon(self):
        """
        Has either team won yet?
        """
        outcome = None

        # Compare teamPoints to threshold
        if self.teamPoints["team1"] > self.pointsToWin:
            if self.teamPoints["team2"] > self.pointsToWin:
                # Both teams have enough, so winner is team with more
                if self.teamPoints["team1"] > self.teamPoints["team2"]: outcome = "team1"
                else: outcome = "team2"
            else:
                # Team 1 wins
                outcome = "team1"
        if self.teamPoints["team2"] > self.pointsToWin:
            # Team 2 wins
            outcome = "team2"

        # TODO print team standings
        # TODO print a big banner when there's a winner
        if outcome: print "\n\n\nWINNER!!! ", outcome
        return outcome

if __name__ == "__main__":
    print("Let's play Spades!")
    #val = raw_input("Enter your value: ")    # convert to input() for python 3.6
    playerName = raw_input("What is your name? ")
    if playerName=="": playerName = "Player 1"

    game = spades()
    game.startGame()