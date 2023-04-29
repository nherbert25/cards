from random import shuffle as r_shuffle


class Card:
    """
    Card class that represents each card in the deck.

    Attributes:
        rank (str): Represents the point value of each card (2 - Ace).
        suit (str): Represents the suit of each card (Hearts, Diamonds, Clubs, Spades).
        image (str): Represents the filepath to each card image that is displayed on the page.

    """

    def __init__(self, rank, suit, image=None):
        self.rank = rank
        self.suit = suit
        self.image = image


class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['S', 'H', 'D', 'C']
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]

    def shuffle(self):
        r_shuffle(self.cards)


player_name = 'Taylor'
dealer_sum = 1
your_sum = 0

dealer_ace_count = 0
your_ace_count = 0


your_cards = []


test_cards = [Card(rank='9', suit='S'), Card(rank='7', suit='D')]