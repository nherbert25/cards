class Card:
    """
    Card class that represents each card in the deck.

    Attributes:
        rank (str): Represents the point value of each card (2 - Ace).
        suit (str): Represents the suit of each card (Hearts, Diamonds, Clubs, Spades).
        image_path (str): Represents the filepath to each card image that is displayed on the page.

    """

    def __init__(self, rank: str, suit: str, hidden: bool = False):
        self._rank = rank
        self._suit = suit
        self._hidden = hidden

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit

    @property
    def rank(self):
        """Get the rank based on whether the card is hidden or not."""
        return None if self.hidden else self._rank

    @property
    def suit(self):
        """Get the suit based on whether the card is hidden or not."""
        return None if self.hidden else self._suit

    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, value: bool):
        self._hidden = value

    @property
    def image(self):
        """Get the image path for the card, either face up or face down."""
        return 'images/playing_cards/BACK.png' if self.hidden else f"images/playing_cards/{self.rank}-{self.suit}.png"

    def flip(self):
        """Flip the card (toggle its hidden state)."""
        self.hidden = not self.hidden

    def to_dict(self):
        """Returns a dictionary representation of the card, based on visibility."""
        return {
            'rank': self.rank,
            'suit': self.suit,
            'image_path': self.image
        }
