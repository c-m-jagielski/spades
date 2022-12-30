# Spades game
from deck import deck

class spades(object):

    playerName = ""
    numPlayers = 4
    d = None

    def startGame(object):
        """
        """
        d = deck()
        deck.deal(d, numPlayers=4, debug=True)

    def reset(object):
        """
        Reset variables in this class
        """
        d = None

if __name__ == "__main__":
    print("Let's play Spades!")

    game = spades()
    game.startGame()