from uuid import UUID, uuid4

from cards.blackjack.hand_model import Hand
from typing import List


class Player:
    def __init__(self, user_id: UUID = None, player_name: str = 'Guest', coins: int = 500, bet: int = 50):
        self.user_id = user_id or uuid4()
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

    def add_hand(self, hand: Hand) -> None:
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
