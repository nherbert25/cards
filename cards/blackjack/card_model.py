class Card:
    """
    Card class that represents each card in the deck.

    Attributes:
        rank (str): Represents the point value of each card (2 - Ace).
        suit (str): Represents the suit of each card (Hearts, Diamonds, Clubs, Spades).
        image_path (str): Represents the filepath to each card image that is displayed on the page.

    """

    def __init__(self, rank: str, suit: str, hidden: bool = False):
        self.rank = rank
        self.suit = suit
        self.image_path = 'images/playing_cards/BACK.png' if hidden else f"images/playing_cards/{self.rank}-{self.suit}.png "

    def to_dict(self):
        return {
            'rank': self.rank,
            'suit': self.suit,
            'image_path': self.image_path
        }