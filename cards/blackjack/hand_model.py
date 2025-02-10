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
        self.cards: List[Card] = []
        self.bet: int = bet
        self.sum: int = 0
        self.has_stayed: bool = False
        self.has_bust: bool = False
        self.has_blackjack: bool = False
        self.win_or_lose_message: str = f'Current bet: {bet}'
        self.outcome: HandOutcome = HandOutcome.NOT_EVALUATED
        self.sum_method: staticmethod = None

    def draw_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        self.cards.remove(card)

    # TODO: function is not currently used. Have blackjack.hit() call this instead
    def hit(self, card: Card, sum_method):
        self.draw_card(card)
        self.get_sum(sum_method)

        if self.sum > self.BLACKJACK_MAX:
            self.hand_busts()

        if self.sum == self.BLACKJACK_MAX:
            if self.check_if_blackjack():
                self.has_blackjack = True
                self.win_or_lose_message = 'Blackjack!'
            self.has_stayed = True

    def stay(self):
        self.has_stayed = True

    def evaluate_outcome(self, outcome: HandOutcome):
        self.outcome = outcome

        if self.outcome == HandOutcome.WIN:
            self.win_or_lose_message = f'You win! +{self.bet} coins!'
        elif self.outcome == HandOutcome.PUSH:
            self.win_or_lose_message = f'You Push!'
        elif self.outcome == HandOutcome.LOSE:
            self.win_or_lose_message = f'You lose! -{self.bet} coins!'

    def get_sum(self, sum_method):
        # Use the injected sum method to calculate the sum
        result = sum_method(self.cards)
        self.sum = result
        return result

    def hand_wins(self) -> None:
        self.win_or_lose_message = f'You win! +{self.bet} coins!'

    def hand_pushes(self) -> None:
        self.win_or_lose_message = f'You Push!'

    def hand_busts(self) -> None:
        self.has_stayed = True
        self.has_bust = True
        self.win_or_lose_message = f'Busted!'

    def hand_loses(self) -> None:
        self.win_or_lose_message = f'You lose! -{self.bet} coins!'

    def check_if_blackjack(self) -> bool:
        return self.calculate_blackjack_sum(self.cards) == self.BLACKJACK_MAX and len(self.cards) == 2

    @staticmethod
    def calculate_blackjack_sum(card_list: List[Card]) -> int:
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