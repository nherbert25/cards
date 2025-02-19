from enum import Enum
from typing import List

from cards.blackjack.card_model import Card


class HandOutcome(Enum):
    WIN = 'win'
    LOSE = 'lose'
    PUSH = 'push'
    NOT_EVALUATED = 'not_evaluated'


class Hand:
    BLACKJACK_MAX = 21

    def __init__(self, bet=50, blackjack_max=None):
        self.BLACKJACK_MAX: int = blackjack_max or Hand.BLACKJACK_MAX
        self._bet: int = bet
        self._sum: int = 0
        self._has_stayed: bool = False
        self._has_bust: bool = False
        self._has_blackjack: bool = False
        self.cards: List[Card] = []
        self.win_or_lose_message: str = f'Current bet: {bet}'
        self.outcome: HandOutcome = HandOutcome.NOT_EVALUATED
        self.sum_method: staticmethod = None

    @property
    def bet(self):
        return self._bet

    @property
    def sum(self):
        return self.calculate_blackjack_sum(self.cards)

    @property
    def has_stayed(self):
        return self._has_stayed

    @property
    def has_bust(self):
        return self._has_bust

    @property
    def has_blackjack(self):
        return self._has_blackjack

    def draw_card(self, card: Card):
        self.cards.append(card)
        if self.sum > self.BLACKJACK_MAX:
            self._hand_busts()
        if self.sum == self.BLACKJACK_MAX:
            if self._check_if_blackjack():
                self._has_blackjack = True

    def discard_card(self, card: Card):
        self.cards.remove(card)

    def hit(self, card: Card):
        self.draw_card(card)

        if self.has_blackjack:
            self.win_or_lose_message = 'Blackjack!'
            self._has_stayed = True

    def stay(self):
        self._has_stayed = True

    def evaluate_outcome(self, outcome: HandOutcome):
        self.outcome = outcome

        if self.outcome == HandOutcome.WIN:
            self.win_or_lose_message = f'You win! +{self.bet} coins!'
        elif self.outcome == HandOutcome.PUSH:
            self.win_or_lose_message = f'You Push!'
        elif self.outcome == HandOutcome.LOSE:
            self.win_or_lose_message = f'You lose! -{self.bet} coins!'

    def _hand_wins(self) -> None:
        self.win_or_lose_message = f'You win! +{self.bet} coins!'

    def _hand_pushes(self) -> None:
        self.win_or_lose_message = f'You Push!'

    def _hand_busts(self) -> None:
        self._has_stayed = True
        self._has_bust = True
        self.win_or_lose_message = f'Busted!'

    def _hand_loses(self) -> None:
        self.win_or_lose_message = f'You lose! -{self.bet} coins!'

    def _check_if_blackjack(self) -> bool:
        return self.sum == self.BLACKJACK_MAX and len(self.cards) == 2

    @staticmethod
    def calculate_blackjack_sum(card_list: List[Card]) -> int:
        result = 0
        ace_count = 0
        for card in card_list:
            if card.rank is None:
                continue
            if card.rank == 'A':
                ace_count += 1
            else:
                if card.rank in ['J', 'Q', 'K']:
                    value = 10
                else:
                    value = int(card.rank)
                result += value
        if ace_count == 1:
            if result + 11 > Hand.BLACKJACK_MAX:
                return result + 1
            else:
                return result + 11
        elif ace_count > 1:
            if result + 11 + ace_count - 1 > Hand.BLACKJACK_MAX:
                return result + ace_count
            else:
                return result + 11 + ace_count - 1
        return result

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
