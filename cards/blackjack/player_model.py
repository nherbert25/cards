from cards.blackjack.card_model import Card
from typing import List


class Player:
    def __init__(self, user_id, player_name='Guest', coins=500):
        self.user_id = user_id
        self.sum = 0
        self.hand: List[Card] = []
        self.coins = coins
        self.player_name = player_name
        self.has_stayed: bool = False
        self.has_bust: bool = False
        self.win_or_lose_message: str = ''

    def draw_card(self, card: Card):
        self.hand.append(card)

    # Serialize for websocket handling
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'sum': self.sum,
            'hand': [Card.to_dict(card) for card in self.hand],
            'coins': self.coins,
            'player_name': self.player_name,
            'has_stayed': self.has_stayed,
            'win_or_lose_message': self.win_or_lose_message
        }
