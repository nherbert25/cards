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

    def method_one(self):
        """
        Some method that does something with the Card object.
        :return:
        """
        pass

    def method_two(self):
        """
        Some method that does something with the Card object.
        :return:
        """
        pass
    