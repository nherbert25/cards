from random import shuffle as r_shuffle
from typing import List


class Card:
    """
    Card class that represents each card in the deck.

    Attributes:
        rank (str): Represents the point value of each card (2 - Ace).
        suit (str): Represents the suit of each card (Hearts, Diamonds, Clubs, Spades).
        image (str): Represents the filepath to each card image that is displayed on the page.

    """

    def __init__(self, rank: str, suit: str, image=None):
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


# Model class for Blackjack game
class BlackjackModel:
    def __init__(self):
        self.your_sum = None
        self.your_cards = None
        self.your_coins = 500
        self.dealer_sum = None
        self.dealer_cards = None
        self.deck = Deck()
        self.player_name = 'Taylor'
        self.game_exists: bool = False

    def start_new_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer_cards = [self.deck.cards.pop()]
        self.dealer_sum = self.calculate_blackjack_sum(self.dealer_cards)
        self.your_cards = [self.deck.cards.pop(), self.deck.cards.pop()]
        self.your_sum = self.calculate_blackjack_sum(self.your_cards)
        self.game_exists = True
        return

    def hit(self):
        self.your_cards.append(self.deck.cards.pop())
        self.your_sum = self.calculate_blackjack_sum(self.your_cards)

    def stay(self):
        # reveal dealer card and have dealer do logic to draw cards

        #compare dealer with user score
            #if you win, gain coins
            #if you lose, lose coins
        if self.your_sum > self.dealer_sum:
            self.you_win()
        else:
            self.you_lose()

        #reset board
        self.start_new_game()

    def you_win(self):
        self.your_coins += 50
        return

    def you_lose(self):
        self.your_coins -= 50
        return

    def calculate_blackjack_sum(self, card_list: List[Card]) -> int:
        my_sum = 0
        ace_count = 0
        for card in card_list:
            if card.rank == 'A':
                ace_count += 1
            else:
                if card.rank in ['J', 'Q', 'K']:
                    value = 10
                else:
                    value = int(card.rank)
                my_sum += value
        if ace_count == 1:
            if my_sum + 11 > 21:
                return my_sum + 1
            else:
                return my_sum + 11
        elif ace_count > 1:
            if my_sum + 11 + ace_count - 1 > 21:
                return my_sum + ace_count
            else:
                return my_sum + 11 + ace_count - 1
        return my_sum
