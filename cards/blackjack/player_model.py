import logging
from uuid import UUID, uuid4

from cards.blackjack.hand_model import Hand, HandOutcome
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

    def add_hand(self, hand: Hand, index: int = None) -> None:
        if index is None:
            self.hands.append(hand)
        else:
            self.hands.insert(index, hand)

    def stay_hand(self, hand_index: int) -> None:
        try:
            self.get_hand(hand_index).stay()
        except IndexError:
            logging.error(f"Attempted to locate hand: {hand_index}. Hand index doesn't exist. {len(self.hands)} in hand.", exc_info=True)  # Log error + traceback
            print(f"Attempted to locate hand: {hand_index}. Hand index doesn't exist. {len(self.hands)} in hand.")
        except Exception as e:
            logging.error(f"Unexpected error locating hand index: {hand_index}", exc_info=True)
            print(f"Unexpected error locating hand index: {hand_index}")

    def split_pair(self, hand_index: int) -> None:
        current_hand = self.get_hand(hand_index)
        if current_hand.can_split_pairs:
            hand_1, hand_2 = current_hand.split_pairs()
            self.add_hand(hand_index+1, hand_2)

    def evaluate_round_end(self):
        payout = 0
        for hand in self.hands:
            if hand.outcome == HandOutcome.WIN:
                payout += hand.bet
            if hand.outcome == HandOutcome.LOSE:
                payout -= hand.bet
        self.coins += payout
        if payout > 0:
            self.win_or_lose_message = f'You win! +{payout} coins!'
        elif payout < 0:
            self.win_or_lose_message = f'You lose! -{payout} coins!'
        elif payout == 0:
            self.win_or_lose_message = f'You Push!'

    def new_round(self, bet):
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
