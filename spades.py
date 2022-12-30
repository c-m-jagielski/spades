# Spades game
from deck import deck

class spades(object):

    playerName = ""
    numPlayers = 4
    d = None
    playerCards = {}

    def startGame(object):
        """
        """
        d = deck()
        playerCards = deck.deal(d, numPlayers=4, debug=True)

    def reset(object):
        """
        Reset variables in this class
        """
        d = None
        playerCards = {}

if __name__ == "__main__":
    print("Let's play Spades!")
    #val = raw_input("Enter your value: ")    # convert to input() for python 3.6
    playerName = raw_input("What is your name? ")
    if playerName=="": playerName = "Player 1"

    game = spades()
    game.startGame()