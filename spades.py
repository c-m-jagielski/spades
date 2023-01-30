# Spades game
from deck import deck
import random, copy, time

class spades(object):

    playerName = ""
    numPlayers = 4
    d = None
    playerCards = {}
    playerBids = {"p1":None, "p2":None, "p3":None, "p4":None}
    yourTeamBid = 0        # For players p1 and p3
    opponentTeamBid = 0    # For players p2 and p4
    spadesUsed = False

    # Modes for playing
    EASY = 1
    HARD = 2
    gameMode = HARD #EASY

    teamPoints = {"team1":0, "team2":0}
    teamSandbags = {"team1":0, "team2":0}
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

            # Account for sandbags
            print "\n\nSandbag Count:"
            print "\tTeam 1: ", self.teamSandbags["team1"]
            print "\tTeam 2: ", self.teamSandbags["team2"]
            if self.teamSandbags["team1"] == 10:
                self.teamSandbags["team1"] = 0
                self.teamPoints["team1"] -= 100
                print "\n\n\nTeam 1 just lost 100 points from sandbags!"
            if self.teamSandbags["team2"] == 10:
                self.teamSandbags["team2"] = 0
                self.teamPoints["team2"] -= 100
                print "\n\n\nTeam 2 just lost 100 points from sandbags!"

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
        if leadUser == "p1":
            # Show the user their hand and get their bid first
            time.sleep(0.2)
            print "You bid first this round."
            time.sleep(0.2)
            self.displayHand(playerCards["p1"])
            time.sleep(0.2)
            self.playerBids['p1'] = self.obtainUserBid()

            # Now CPU's will bid
            self.playerBids['p2'] = self.obtainCpuBid(playerCards["p2"])
            self.playerBids['p3'] = self.obtainCpuBid(playerCards["p3"])
            self.playerBids['p4'] = self.obtainCpuBid(playerCards["p4"])

        elif leadUser == "p2":
            self.playerBids['p2'] = self.obtainCpuBid(playerCards["p2"])
            self.playerBids['p3'] = self.obtainCpuBid(playerCards["p3"])
            self.playerBids['p4'] = self.obtainCpuBid(playerCards["p4"])

            # Show the user their hand and get their bid
            print " "
            time.sleep(.5)
            print "P 2 bid: ", p2bid
            time.sleep(.1)
            print "P 3 bid: ", p3bid
            time.sleep(.1)
            print "P 4 bid: ", p4bid
            time.sleep(.5)

            self.displayHand(playerCards["p1"])
            self.playerBids['p1'] = self.obtainUserBid()

        elif leadUser == "p3":
            self.playerBids['p3'] = self.obtainCpuBid(playerCards["p3"])
            self.playerBids['p4'] = self.obtainCpuBid(playerCards["p4"])

            # Show the user their hand and get their bid
            print " "
            time.sleep(.5)
            print "P 3 bid: ", p3bid
            time.sleep(.1)
            print "P 4 bid: ", p4bid
            time.sleep(.5)
            self.displayHand(playerCards["p1"])
            self.playerBids['p1'] = self.obtainUserBid()

            self.playerBids['p2'] = self.obtainCpuBid(playerCards["p2"])

        elif leadUser == "p4":
            self.playerBids['p4'] = self.obtainCpuBid(playerCards["p4"])

            # Show the user their hand and get their bid
            print " "
            time.sleep(.5)
            print "P 4 bid: ", p4bid
            time.sleep(.5)
            self.displayHand(playerCards["p1"])
            self.playerBids['p1'] = self.obtainUserBid()

            self.playerBids['p2'] = self.obtainCpuBid(playerCards["p2"])
            self.playerBids['p3'] = self.obtainCpuBid(playerCards["p3"])
        else: pass

        # Display the bids to the user
        print " "
        time.sleep(.5)
        print "You bid: ", self.playerBids['p1']
        time.sleep(.1)
        print "P 2 bid: ", self.playerBids['p2']
        time.sleep(.1)
        print "P 3 bid: ", self.playerBids['p3']
        time.sleep(.1)
        print "P 4 bid: ", self.playerBids['p4']
        time.sleep(.3)

        # Calculate team bids for this roundCards
        self.yourTeamBid = self.playerBids['p1'] + self.playerBids['p3']
        self.opponentTeamBid = self.playerBids['p2'] + self.playerBids['p4']
        print " "
        print "Your Team bid: ", self.yourTeamBid
        time.sleep(.1)
        print "Their Team bid: ", self.opponentTeamBid
        time.sleep(.5)

        # A round has 13 hands to play in order to add up all the tricks
        trickTotals = {"p1":0, "p2":0, "p3":0, "p4":0}
        for r in range(1,14):
            winner = self.playHand(previousRoundWinner, playerCards, trickTotals)
            trickTotals[winner] += 1
            previousRoundWinner = copy.deepcopy(winner)

        # Calculate points for this round; calculate sandbags; subtract if bid not met
        team1Total = trickTotals["p1"] + trickTotals["p3"]
        team2Total = trickTotals["p2"] + trickTotals["p4"]
        team1Score = 0
        team2Score = 0
        if team1Total >= self.yourTeamBid:
            self.teamSandbags["team1"] += (team1Total - self.yourTeamBid)
            team1Score = 10 * team1Total
        else: team1Score = -10 * team1Total
        if team2Total >= self.opponentTeamBid:
            self.teamSandbags["team2"] += (team2Total - self.opponentTeamBid)
            team2Score = 10 * team2Total
        else: team2Score = -10 * team2Total

        roundPoints = {"team1": team1Score, "team2": team2Score}
        return roundPoints

    def playHand(self, leadUser, playerCards, trickTotals):
        """
        Play a single hand, each player submits a card and somebody wins the trick.
        """
        roundCards = {}
        leadSuit = None

        time.sleep(1.5)
        print "\n__________________________________________________________________"
        print "\t\tYour team has", trickTotals["p1"] + trickTotals["p3"], "tricks.\tYou bid", self.yourTeamBid
        print "\t\tOpponent has", trickTotals["p2"] + trickTotals["p4"], "tricks.\tThey bid", self.opponentTeamBid
        print "__________________________________________________________________\n"

        if leadUser == "p1":
            print "You have the lead this hand."
            roundCards["p1"] = self.userLeads(playerCards["p1"])
            leadSuit = roundCards[leadUser]["suit"]

            # Time for CPU's to play
            roundCards["p2"] = self.selectCPUCard(playerCards["p2"], roundCards, leadSuit, leadUser, 'p2', trickTotals)
            roundCards["p3"] = self.selectCPUCard(playerCards["p3"], roundCards, leadSuit, leadUser, 'p3', trickTotals)
            roundCards["p4"] = self.selectCPUCard(playerCards["p4"], roundCards, leadSuit, leadUser, 'p4', trickTotals)

        if leadUser == "p2":
            print "Player 2 has the lead this hand."
            roundCards["p2"] = self.selectCPULeadCard(playerCards["p2"], 'p2', trickTotals)
            leadSuit = roundCards[leadUser]["suit"]

            roundCards["p3"] = self.selectCPUCard(playerCards["p3"], roundCards, leadSuit, leadUser, 'p3', trickTotals)
            roundCards["p4"] = self.selectCPUCard(playerCards["p4"], roundCards, leadSuit, leadUser, 'p4', trickTotals)
            roundCards["p1"] = self.userPlays(playerCards["p1"], leadSuit)

        if leadUser == "p3":
            print "Player 3 has the lead this hand."
            roundCards["p3"] = self.selectCPULeadCard(playerCards["p3"], 'p3', trickTotals)
            leadSuit = roundCards[leadUser]["suit"]

            roundCards["p4"] = self.selectCPUCard(playerCards["p4"], roundCards, leadSuit, leadUser, 'p4', trickTotals)
            roundCards["p1"] = self.userPlays(playerCards["p1"], leadSuit)
            roundCards["p2"] = self.selectCPUCard(playerCards["p2"], roundCards, leadSuit, leadUser, 'p2', trickTotals)

        if leadUser == "p4":
            print "Player 4 has the lead this hand."
            roundCards["p4"] = self.selectCPULeadCard(playerCards["p4"], 'p4', trickTotals)
            leadSuit = roundCards[leadUser]["suit"]

            roundCards["p1"] = self.userPlays(playerCards["p1"], leadSuit)
            roundCards["p2"] = self.selectCPUCard(playerCards["p2"], roundCards, leadSuit, leadUser, 'p2', trickTotals)
            roundCards["p3"] = self.selectCPUCard(playerCards["p3"], roundCards, leadSuit, leadUser, 'p3', trickTotals)

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
        cardSelection = 0
        while 1:
            try:
                cardSelection = int(raw_input("\n\nWhat card will you play? ")) - 1
            except ValueError:
                time.sleep(0.2)
                print "...."
                print "Please enter an INTEGER for your hand.\n"
                time.sleep(0.1)
                continue
            else:
                break

        # Is the user's selection allowed?
        isAllowed = self.checkPlayedCard(usersHand, cardSelection, leadSuit)
        if not isAllowed:
            self.prepareResponse()
            print "\n\nYour selection is not allowed. Try again."
            cardSelection = int(raw_input("\n\nWhat card will you play? ")) - 1

        cardSelected = usersHand[cardSelection]
        usersHand.pop(cardSelection)
        return cardSelected

    def selectCPUCard(self, hand, roundCards, leadSuit, leadPlayer, whoAmI, trickTotals):
        """
        CPU will select a valid card to play.
        This function is not for when a CPU user is the lead initiating a round.

        If CPU user has same suit as lead suit, must play that.
        If CPU user does not have same suit as lead suit, can play anything.

        hand: [input] the current user's full hand of cards
        roundCards: [input] dict of current cards already played this round
        leadSuit: [input] suit that was lead this round
        leadPlayer: [input] player that lead this round
        whoAmI: [input] string of who this CPU user is
        trickTotals: [input] dict of current trick totals for each player
        """
        selection = None

        """
        print "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        print "CPU USER: \t", whoAmI
        print "CPU Hand: \t", len(hand)
        #print "CPU hand: \t", hand
        #print "Lead suit: \t", leadSuit
        #print "Round cards: \t", roundCards
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
        """

        # User must play the suited card if they have it
        ableToPlay = []
        for i in range(0, len(hand)):
            if hand[i]["suit"] == leadSuit: ableToPlay.append(hand[i])

        if len(ableToPlay) < 1:
            ableToPlay = copy.deepcopy(hand)
        #print "ableToPlay: ", ableToPlay

        # By default start out with a random card
        ableIndex = random.randint(0,len(ableToPlay)-1)

        # In HARD mode, purposefully choose which card to play
        if self.gameMode == self.HARD:
            winDesire = self.doIWantToWinThisHand(whoAmI, trickTotals)
            print "CPU ", whoAmI, " Win Desire: ", winDesire

        selection = ableToPlay[ableIndex]
        #print "selection: ", selection
        #print "ableIndex: \t", ableIndex

        for i in range(0, len(hand)):
            if hand[i] == selection:
                #print "about to pop hand[i]: ", hand[i]
                hand.pop(i)
                break

        print "\nPlayer", whoAmI, "played the", selection['value'], "of", selection['suit']
        time.sleep(0.35)
        return selection

    def selectCPULeadCard(self, hand, whoAmI, trickTotals):
        """
        Select the lead card the CPU player will play for a given hand.

        In EASY mode, make it random.
        In HARD mode, purposefully choose which card to lead with.
        """

        """
        print "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        print "CPU USER: \t", whoAmI
        print "CPU Hand: \t", len(hand)
        #print "CPU hand: \t", hand
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
        """

        ableToPlay = []

        if self.spadesUsed:
            # Can lead with anything
            ableToPlay = copy.deepcopy(hand)
        else:
            for i in range(0, len(hand)):
                if hand[i]["suit"] != 'spades': ableToPlay.append(hand[i])

        # Initialize the chosen card with something random
        i = random.randint(0,len(ableToPlay)-1)

        # Do advanced calculations for HARD mode only when we have more than 1 option to play.
        if self.gameMode == self.HARD and len(ableToPlay) > 1:
            # Purposefully choose which card to play
            winDesire = self.doIWantToWinThisHand(whoAmI, trickTotals)
            print "CPU ", whoAmI, " Lead Win Desire: ", winDesire

            # Do I have a Spade in my hand?
            ableToLeadSpade = False
            for ii in range(1, len(ableToPlay)):
                if ableToPlay[ii]["suit"] == "spades":
                    ableToLeadSpade = True
                    break

            # Count cards to determine win probability with what I have!!!
            # Will make the CPU very smart..... until then, do some simple logic.
            # TODO

            # Figure out which cards will win (or might win) and choose one now
            if winDesire == 0:
                # Lead the lowest non-spade (if possible)
                # Pick the first card and see if anything is lower than it
                tmpCard = ableToPlay[0]
                i = 0
                for ii in range(1, len(ableToPlay)):
                    if ableToPlay[ii]["rank"] < tmpCard["rank"]:
                        print "DEBUG: CPU was going to lead with ", tmpCard, "but is now going to lead with ", ableToPlay[ii]
                        tmpCard = ableToPlay[ii]
                        i = ii
            elif winDesire == 1:
                # Pick the best card with which to lead.

                if len(hand) > 10:
                    # If early in the game, can lead with an ACE without too much risk.
                    for ii in range(0, len(ableToPlay)):
                        if ableToPlay[ii]["value"] == "A":
                            print "DEBUG: CPU going to lead with ", ableToPlay[ii]
                            i = ii
                            break
                elif ableToLeadSpade:
                    # Lead with a high spade is a near-guaranteed win.
                    tmpCard = ableToPlay[0]
                    i = 0
                    for ii in range(1, len(ableToPlay)):
                        if ableToPlay[ii]["suit"] == "spades" and ableToPlay[ii]["rank"] > tmpCard["rank"]:
                            print "DEBUG: CPU was going to lead with ", tmpCard, "but is now going to lead with ", ableToPlay[ii]
                            tmpCard = ableToPlay[ii]
                            i = ii
                else:
                    # Pick highest overall card
                    # TODO
                    pass
            elif winDesire < 0.5:
                # Win Desire is between 0.0 and 0.5, so pick something low but not my lowest
                # TODO make this scale somehow

                # Find the lowest rank then throw that away from my options.
                adjustedAbleToPlay = {}
                lowestRank = 999
                for ii in range(1, len(ableToPlay)):
                    if ableToPlay[ii]["rank"] > lowestRank: lowestRank = ableToPlay[ii]["rank"]
                for ii in range(1, len(ableToPlay)):
                    if ableToPlay[ii]["rank"] > lowestRank: adjustedAbleToPlay.append(ableToPlay[ii])

                # Find the lowest now from my adjusted list, and lead with that.
                tmpCard = adjustedAbleToPlay[0]
                i = 0
                for ii in range(1, len(adjustedAbleToPlay)):
                    if adjustedAbleToPlay[ii]["rank"] < tmpCard["rank"]:
                        print "DEBUG: CPU was going to lead with ", tmpCard, "but is now going to lead with ", adjustedAbleToPlay[ii]
                        tmpCard = adjustedAbleToPlay[ii]
                        i = ii
            else:
                # Win Desire is between 0.5 and 1.0, so pick something high but not my highest
                # TODO
                pass

        selection = ableToPlay[i]
        hand.pop(i)
        print "\nPlayer", whoAmI, "lead with the", selection['value'], "of", selection['suit']
        time.sleep(0.35)
        return selection

    def selectRoundWinner(self, roundCards, leadSuit):
        """
        Determine which player wins this round and obtains a hand.
        """
        #print "\n\n\n"
        #print "\tleadSuit: ", leadSuit
        #print "\troundCards: ", roundCards

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
        #print "###\twinner: ", winner
        for i in range(1, len(eligibleCards)):
            if eligibleCards[i]["index"] > winner["index"]: winner = eligibleCards[i]
            #print "###\twinner: ", winner

        # Find the user that won the hand
        winningUser = None
        for i in ["p1", "p2", "p3", "p4"]:
            if roundCards[i] == winner:
                winningUser = i
                break
        time.sleep(0.2)
        print "\nWinner:   ", winningUser
        time.sleep(0.2)
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

    def doIWantToWinThisHand(self, whoAmI, trickTotals):
        """
        Optimize if the CPU wants to win this hand or not.
        Returns integer that is later used to choose which card to use to win.
            0.0 - this is 0% want-to-win, so by all means try to *not* win the hand
            0.5 - this is 50/50, basically either is fine
            1.0 - this is 100% must win, so do everything possible to win
            else- TODO ... some advanced way to determine preferences/strategy...
                - for example if 0.8 is returned, then perhaps you can try to win with a
                  _somewhat_ strong card, but not necessary your best card (don't waste
                  an Ace of Spades on an 0.8 unless that's all you have left)
        """

        # If this CPU player went nill, return 0.0
        if self.playerBids[whoAmI] == 0: return 0.0

        # Set up local variables to use
        myTeamMate = "p1"
        if whoAmI == "p2": myTeamMate = "p4"
        if whoAmI == "p4": myTeamMate = "p2"

        # If my team mate went nill and they're currently winning the hand, return 1.0
        #if self.playerBids[myTeamMate] == 0 and .....
        #TODO

        # Does our team still need to win any more tricks this game?
        haveNotMetBid = False
        if whoAmI == "p2":
            if (trickTotals["p2"] + trickTotals["p4"]) < self.opponentTeamBid: haveNotMetBid = True
        else:
            if (trickTotals["p1"] + trickTotals["p3"]) < self.yourTeamBid: haveNotMetBid = True

        # If our team needs to win tricks, do I want to win this one
        # or do I have the ability to win enough later? I.e. Ace of Spades guaranteed win
        # TODO

        # Would I like to try and set my opponents?
        # TODO

        # Choice depends on player position this hand (leading, 2nd, 3rd, or last)...
        # TODO

        return 1.0

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
        time.sleep(0.2)
        print "\n\n**** **** **** **** **** **** ****"
        print "          YOUR HAND\n**** **** **** **** **** **** ****"
        time.sleep(0.1)

        i = 0
        while i < len(inputCards):
            print i+1, ")\t", inputCards[i]["value"], "\t", inputCards[i]["suit"]
            i += 1
        print " "
        time.sleep(0.2)

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
        """
        Algorithm to determine the bid of a CPU player.
        Bid is randomly chosen in EASY mode, implying the CPU doesn't know what it's doing
        and can easily mess up during the game.
        """

        # Easy mode will randomly choose a low/reasonable number
        if self.gameMode == self.EASY: return random.randint(1,4)

        # Hard mode
        bid = 0

        # Go through their hand to obtain a few metrics.
        numSpades = 0
        numHearts = 0
        numDiamonds = 0
        numClubs = 0
        queenOrHigher = 0
        spadesAbove7 = 0

        for i in range(0, 13):
            card = hand[i]
            if card['suit'] == 'spades':
                numSpades += 1
                if card['value'] not in ['1', '2', '3', '4', '5', '6', '7']:
                    spadesAbove7 += 1
            if card['suit'] == 'hearts': numHearts += 1
            if card['suit'] == 'diamonds': numDiamonds += 1
            if card['suit'] == 'clubs': numClubs += 1
            if card['value'] == 'Q': queenOrHigher += 1
            if card['value'] == 'K': queenOrHigher += 1
            if card['value'] == 'A': queenOrHigher += 1

        # If user has a few high spades, need to bid a certain amount since it's very
        # likely to win those hands.
        # TODO
        #if

        # Let the CPU go nill under certain very conservative conditions.
        # No spades, & nothing higher than Jack in any suit.
        if numSpades == 0 and queenOrHigher == 0: return 0
        # Only 1 spade, which is 7 or lower, and only 1 other suited card above Jack.
        if numSpades < 2 and spadesAbove7 == 0 and queenOrHigher < 2: return 0

        #DEBUG... this is a last resort to prevent the game from crashing
        return random.randint(1,4)

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

        # Print team standings
        print "\n\n"
        print "------ ------ ------ ------"
        print "       Team 1:      ", self.teamPoints["team1"]
        print "       Team 2:      ", self.teamPoints["team2"]
        print "------ ------ ------ ------"
        print " "

        # Compare teamPoints to threshold
        if self.teamPoints["team1"] > self.pointsToWin:
            if self.teamPoints["team2"] > self.pointsToWin:
                # Both teams have enough, so winner is team with more
                if self.teamPoints["team1"] > self.teamPoints["team2"]: outcome = "team1"
                else: outcome = "team2"
            else:
                # Team 1 wins
                outcome = "team1"
        elif self.teamPoints["team2"] > self.pointsToWin:
            # Team 2 wins
            outcome = "team2"
        else: pass

        # Print a big banner when there's a winner
        if outcome:
            print "******************************************************"
            print "******************************************************"
            print "******************************************************"
            print "\n\n\nWINNER!!! ", outcome
            print "\n\n"
            print "******************************************************"
            print "******************************************************"
            print "******************************************************"

        return outcome

if __name__ == "__main__":
    print("Let's play Spades!")
    time.sleep(0.1)
    #val = raw_input("Enter your value: ")    # convert to input() for python 3.6
    playerName = raw_input("What is your name? ")
    if playerName=="": playerName = "Player 1"

    game = spades()
    game.startGame()