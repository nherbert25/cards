from card import Card
import random


class Deck:
    """
    Deck class that represents a collection of 52 Cards.

    Attributes:
        cards (int): Represents the total number of cards remaining in the deck.

    Methods:
        shuffle(): A method that randomly shuffles the order of Cards in the Deck.
    """

    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]

    def shuffle(self):
        """
        Randomly shuffles the cards in the deck.
        :return: Returns shuffled deck of cards.
        """
        random.shuffle(self.cards)

    def method_two(self):
        """
        Some method that does something with the Card object.
        :return:
        """
        pass
    