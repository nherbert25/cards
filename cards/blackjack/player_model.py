import logging
from uuid import UUID, uuid4

from cards.blackjack.hand_model import Hand, HandOutcome
from typing import List, Tuple

from cards.database.models import Blackjack
from cards.database.blackjack_table_DAO import BlackjackTableDAO


class Player:
    def __init__(self, user_id: UUID = None, player_name: str = 'Guest', bet: int = 50, dao=None):
        self.user_id = user_id or uuid4()
        self.dao = dao or BlackjackTableDAO()
        self.player_name = player_name
        self.coins = self._get_coins_from_db()
        self.hands: List[Hand] = []
        self.bet = bet
        self.win_or_lose_message: str = f'Current bet: {bet}'
        self._add_new_user_to_blackjack_table()

    def __repr__(self):
        return f'user_id={self.user_id}, name={self.player_name}'

    def _add_new_user_to_blackjack_table(self) -> None:
        database_entry = self.dao.get_user_by_uuid(str(self.user_id))
        if not database_entry:
            new_user = Blackjack(user_uuid=str(self.user_id), coins=500)
            self.dao.add_user_to_database(new_user)

    def _get_coins_from_db(self) -> int:
        database_entry = self.dao.get_user_by_uuid(str(self.user_id))
        if database_entry:
            return database_entry.coins
        return 500

    def _push_coins_to_db(self, coin_change) -> None:
        self.dao.update_coins(str(self.user_id), coin_change)

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
            logging.error(
                f"Attempted to locate hand: {hand_index}. Hand index doesn't exist. {len(self.hands)} in hand.",
                exc_info=True)  # Log error + traceback
            print(f"Attempted to locate hand: {hand_index}. Hand index doesn't exist. {len(self.hands)} in hand.")
        except Exception as e:
            logging.error(f"Unexpected error locating hand index: {hand_index}", exc_info=True)
            print(f"Unexpected error locating hand index: {hand_index}")

    def split_pair(self, hand_index: int) -> bool:
        current_hand = self.get_hand(hand_index)
        if current_hand.can_split_pair:
            hand_1, hand_2 = current_hand.split_pair()
            self.add_hand(hand_2, hand_index + 1)
            return True
        return False

    def evaluate_round_end(self):
        payout = 0
        for hand in self.hands:
            if hand.outcome == HandOutcome.WIN:
                payout += hand.bet
            if hand.outcome == HandOutcome.LOSE:
                payout -= hand.bet
        self.coins += payout
        self._push_coins_to_db(payout)
        self.coins = self._get_coins_from_db()
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
    def to_dict(self) -> dict:
        return {
            "player_name": self.player_name,
            "hands": [hand.to_dict() for hand in self.hands],
            "bet": self.bet,
            "coins": self.coins,
            "win_or_lose_message": self.win_or_lose_message,
        }
