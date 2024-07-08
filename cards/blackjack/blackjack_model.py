from random import shuffle as r_shuffle
from typing import List


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


class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['S', 'H', 'D', 'C']
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]

    def shuffle(self):
        r_shuffle(self.cards)


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
        self.has_stayed: bool = False
        self.BET = 50
        self.win_or_lose_message = None

    def start_new_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer_cards = [Card('0', 'None', hidden=True), self.deck.cards.pop()]
        self.dealer_sum = self.calculate_blackjack_sum(self.dealer_cards)
        self.your_cards = [self.deck.cards.pop(), self.deck.cards.pop()]
        self.your_sum = self.calculate_blackjack_sum(self.your_cards)
        self.game_exists = True
        self.has_stayed = False
        self.win_or_lose_message = None
        return

    def hit(self):
        self.your_cards.append(self.deck.cards.pop())
        self.your_sum = self.calculate_blackjack_sum(self.your_cards)
        if self.your_sum > 21:
            self.you_lose()

    def stay(self):
        self.has_stayed = True
        self.dealer_sum = self.resolve_dealer_turn(self.dealer_cards)
        self.resolve_winner(self.your_sum, self.dealer_sum)

    def resolve_winner(self, your_sum, dealer_sum):
        if your_sum > 21:
            self.you_lose()
        elif dealer_sum > 21:
            self.you_win()
        elif your_sum > dealer_sum:
            self.you_win()
        else:
            self.you_lose()

    def you_win(self):
        self.your_coins += self.BET
        self.win_or_lose_message = f'You win! +{self.BET} coins!'

    def you_lose(self):
        self.your_coins -= self.BET
        self.win_or_lose_message = f'You lose! -{self.BET} coins!'

    def resolve_dealer_turn(self, dealer_cards: List[Card]) -> int:
        flip_face_down_card = self.deck.cards.pop()
        dealer_cards[0] = flip_face_down_card

        dealer_sum = self.calculate_blackjack_sum(dealer_cards)
        while dealer_sum < 17:
            dealer_cards.append(self.deck.cards.pop())
            dealer_sum = self.calculate_blackjack_sum(dealer_cards)

        return dealer_sum

    def calculate_blackjack_sum(self, card_list: List[Card]) -> int:
        result = 0
        ace_count = 0
        for card in card_list:
            if card.rank == 'A':
                ace_count += 1
            else:
                if card.rank in ['J', 'Q', 'K']:
                    value = 10
                else:
                    value = int(card.rank)
                result += value
        if ace_count == 1:
            if result + 11 > 21:
                return result + 1
            else:
                return result + 11
        elif ace_count > 1:
            if result + 11 + ace_count - 1 > 21:
                return result + ace_count
            else:
                return result + 11 + ace_count - 1
        return result
