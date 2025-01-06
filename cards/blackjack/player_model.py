from enum import Enum
from uuid import UUID, uuid4

from flask import jsonify

from cards.blackjack.card_model import Card
from typing import List


class HandOutcome(Enum):
    WIN = 'win'
    LOSE = 'lose'
    PUSH = 'push'
    NOT_EVALUATED = 'not_evaluated'


class Hand:
    def __init__(self, bet=50):
        self.cards: List[Card] = []
        self.bet = bet
        self.sum = 0
        self.has_stayed: bool = False
        self.has_blackjack: bool = False
        self.win_or_lose_message: str = ''
        self.outcome: HandOutcome = HandOutcome.NOT_EVALUATED

    def draw_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        self.cards.remove(card)

    def get_total(self) -> int:
        return sum(card.value for card in self.cards)

    def hand_busts(self) -> None:
        self.win_or_lose_message = f'Busted!'

    def hand_wins(self) -> None:
        self.win_or_lose_message = f'You win! +{self.bet} coins!'

    def hand_pushes(self) -> None:
        self.win_or_lose_message = f'You Push!'

    def hand_loses(self) -> None:
        self.win_or_lose_message = f'You lose! -{self.bet} coins!'

    # Serialize for websocket handling
    def to_dict(self) -> dict:
        return {
            "cards": [card.to_dict() for card in self.cards],  # Assuming Card has a to_dict() method
            "bet": self.bet,
            "sum": self.sum,
            "has_stayed": self.has_stayed,
            "has_blackjack": self.has_blackjack,
            "win_or_lose_message": self.win_or_lose_message,
            "outcome": self.outcome.name  # Assuming HandOutcome is an Enum
        }


class Player:
    def __init__(self, user_id: UUID = None, player_name: str = 'Guest', coins: int = 500, bet: int = 50):
        if user_id is None:
            user_id = uuid4()

        self.user_id = user_id
        self.player_name = player_name
        self.coins = coins
        self.hands: List[Hand] = []
        self.bet = bet
        self.win_or_lose_message: str = f'Current bet: {bet}'

    def __repr__(self):
        return f'user_id={self.user_id}, name={self.player_name}'

    def get_hand(self, hand_index: int) -> Hand:
        if 0 <= hand_index < len(self.hands):
            return self.hands[hand_index]
        raise IndexError(f"Hand index {hand_index} is out of bounds.")

    def add_hand(self, hand: Hand):
        self.hands.append(hand)

    def evaluate_round_end(self):
        pass

    # TODO: implement this
    def new_round(self, bet):
        self.player_outcome = None
        self.bet = bet
        self.win_or_lose_message = f'Current bet: {self.bet}'
        self.hands = []

    # Serialize for websocket handling
    def to_dict(self):
        return {
            'user_id': str(self.user_id),
            'hands': [hand.to_dict() for hand in self.hands],
            'coins': self.coins,
            'player_name': self.player_name,
            'win_or_lose_message': self.win_or_lose_message
        }
