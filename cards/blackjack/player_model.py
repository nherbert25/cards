from uuid import UUID, uuid4

from cards.blackjack.card_model import Card
from typing import List


class Player:
    def __init__(self, user_id: UUID = None, player_name: str = 'Guest', coins: int = 500):
        if user_id is None:
            user_id = uuid4()

        self.user_id = user_id
        self.sum = 0
        self.hand: List[Card] = []
        self.coins = coins
        self.player_name = player_name
        self.has_stayed: bool = False
        self.has_bust: bool = False
        self.has_blackjack: bool = False
        self.win_or_lose_message: str = ''

    def __repr__(self):
        return f'user_id={self.user_id}, name={self.player_name}'

    def draw_card(self, card: Card):
        self.hand.append(card)

    # Serialize for websocket handling
    def to_dict(self):
        return {
            'user_id': str(self.user_id),
            'sum': self.sum,
            'hand': [Card.to_dict(card) for card in self.hand],
            'coins': self.coins,
            'player_name': self.player_name,
            'has_stayed': self.has_stayed,
            'win_or_lose_message': self.win_or_lose_message
        }
