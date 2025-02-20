from copy import deepcopy
from enum import Enum
from typing import List, Optional, Tuple

from cards.blackjack.card_model import Card


class HandOutcome(Enum):
    WIN = 'win'
    LOSE = 'lose'
    PUSH = 'push'
    NOT_EVALUATED = 'not_evaluated'


class Hand:
    BLACKJACK_MAX = 21

    def __init__(self, bet=50, blackjack_max: Optional[int] = None, cards: Optional[list[Card]] = None):
        self.BLACKJACK_MAX: int = blackjack_max or Hand.BLACKJACK_MAX
        self._bet: int = bet
        self._has_stayed: bool = False
        self.cards: List[Card] = cards or []
        self.win_or_lose_message: str = f'Current bet: {self.bet}'
        self.outcome: HandOutcome = HandOutcome.NOT_EVALUATED

    def __getitem__(self, index: int) -> Card:
        return self.cards[index]

    @property
    def bet(self):
        return self._bet

    @bet.setter
    def bet(self, new_bet):
        if new_bet < 0:
            raise ValueError("Bet cannot be negative")
        self._bet = new_bet
        self.win_or_lose_message = f'Current bet: {self.bet}'

    @property
    def sum(self):
        return self.calculate_blackjack_sum(self.cards)

    @property
    def has_stayed(self):
        if self.sum >= self.BLACKJACK_MAX:
            self._has_stayed = True
        return self._has_stayed

    @property
    def has_bust(self):
        return self.sum > self.BLACKJACK_MAX

    @property
    def has_blackjack(self):
        return self.sum == self.BLACKJACK_MAX and len(self.cards) == 2

    @property
    def can_split_pair(self) -> bool:
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

    def hit(self, card: Card) -> None:
        self.draw_card(card)

        if self.has_bust:
            self._hand_busts()

        if self.has_blackjack:
            self.win_or_lose_message = 'Blackjack!'

    def stay(self):
        self._has_stayed = True

    def split_pair(self) -> Tuple["Hand", "Hand"] | None:
        if not self.can_split_pair:
            print('Cannot split!')
            return None
        else:
            new_hand = deepcopy(self)
            new_hand.cards.clear()
            new_hand.hit(self.cards[1])
            self.remove_card(self.cards[1])
            return self, new_hand

    def evaluate_outcome(self, outcome: HandOutcome):
        self.outcome = outcome

        if self.outcome == HandOutcome.WIN:
            self.win_or_lose_message = f'You win! +{self.bet} coins!'
        elif self.outcome == HandOutcome.PUSH:
            self.win_or_lose_message = f'You Push!'
        elif self.outcome == HandOutcome.LOSE:
            self.win_or_lose_message = f'You lose! -{self.bet} coins!'

    def draw_card(self, card: Card) -> None:
        self.cards.append(card)

    def remove_card(self, card: Optional[Card] = None, index: Optional[int] = None) -> Card:
        if index is not None:
            if index < 0 or index > len(self.cards) - 1:
                raise IndexError(f"Cannot remove card, index is invalid. Hand size: {len(self.hands)}, Index: {index}")
            return self.cards.pop(index)
        elif card is not None:
            return self.cards.remove(card)
        else:
            return self.cards.pop()

    def get_card(self, card: Optional[Card] = None, index: Optional[int] = None) -> Card:
        if index is not None:
            if index < 0 or index > len(self.cards) - 1:
                raise IndexError(f"Cannot find card, index is invalid. Hand size: {len(self.hands)}, Index: {index}")
            return self.cards[index]
        elif card is not None:
            return self.cards.remove(card)
        else:
            return self.cards.pop()

    def _hand_wins(self) -> None:
        self.win_or_lose_message = f'You win! +{self.bet} coins!'

    def _hand_pushes(self) -> None:
        self.win_or_lose_message = f'You Push!'

    def _hand_busts(self) -> None:
        self.win_or_lose_message = f'Busted!'

    def _hand_loses(self) -> None:
        self.win_or_lose_message = f'You lose! -{self.bet} coins!'

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
