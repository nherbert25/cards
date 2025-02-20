from enum import Enum
from typing import List, Dict, Optional
from uuid import UUID, uuid4

from cards.blackjack.player_model import Player
from cards.blackjack.hand_model import Hand, HandOutcome
from cards.blackjack.card_model import Card
from cards.blackjack.deck_model import Deck


class GameConfigs:
    # Game configs:
    NUMBER_OF_DECKS = 1
    BLACKJACK_RATIO = 1.5  # Standard payouts for a blackjack (Ace + 10-value card) are 3:2, but some tables pay 6:5, which increases the house edge.


    # Variants
    DEALER_HITS_ON_SOFT_17 = False  # Dealers must hit on soft 17 (Ace + 6) or stand on all 17s, depending on the casino’s rules. Soft Hand: A hand containing an Ace counted as 11. For example, Ace + 6 = "Soft 17."
    RESTRICTED_DOUBLING = False  # Some tables limit doubling down to totals of 9, 10, or 11.

    ALLOW_SPLIT_PAIR = True
    SPLITTING_ACES_ADDITIONAL_RULES = False  # Only one additional card per split Ace. Blackjack is usually not recognized on split Aces (it pays 1:1, not 3:2).
    SPLITTING_RESTRICTIONS = False  # Some tables disallow splitting certain pairs, though this is rare.

    FIVE_CARD_CHARLIE = False  # player automatically wins if they draw five cards without busting. Example: A hand of 4 + 2 + 2 + 2 + 3 = 13 wins against the dealer,
    DEALER_PEEK = False
    """
    If the dealer's face up card is an Ace or a 10-value card, the dealer checks (or "peeks") for blackjack before the player makes decisions like doubling, splitting, or surrendering.
    If the dealer has blackjack, the hand ends immediately, and side bets (e.g., insurance) are resolved.
    If no peek rule is in effect, players risk losing additional bets made on doubles or splits.
    """

    # Side bets:
    ENABLE_PERFECT_PAIR = False  # Bet that your initial two cards will form a pair.
    ENABLE_21_PLUS_3 = False  # Bet on a combination of your cards and the dealer’s upcard forming a poker hand (e.g., flush, straight).
    ENABLE_LUCKY_LUCKY = False  # Bet on your initial hand and the dealer’s upcard creating specific totals or combinations.


class BlackjackModel:
    BLACKJACK_MAX = 21
    DEALER_HOLD_THRESHOLD = 17
    DOUBLE_DOWN_RATIO = 2  # How much a player wins/loses if they double down on a bet

    def __init__(self, game_configs: GameConfigs):
        self.MINIMUM_BET = 50
        self.dealer = None

        self.deck = Deck()
        self.game_exists: bool = False

        # Unpack the game_configs attributes into the class instance
        self.__dict__.update(game_configs.__dict__)

        self.players: Dict[UUID, Player] = {
            player.user_id: player for player in
            [
                Player(player_name='Taylor', user_id=UUID("11111111-1111-1111-1111-111111111111"),
                       bet=self.MINIMUM_BET),
                Player(player_name='Nate', user_id=UUID("22222222-2222-2222-2222-222222222222"), bet=self.MINIMUM_BET),
                Player(player_name='Travis', user_id=UUID("33333333-3333-3333-3333-333333333333"),
                       bet=self.MINIMUM_BET),
            ]
        }

    def start_new_game(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()

        self.dealer = Hand(blackjack_max=self.BLACKJACK_MAX)
        self.dealer.draw_card(self.deck.cards.pop())
        self.dealer.cards[0].flip()
        self.dealer.draw_card(self.deck.cards.pop())

        for player in self.players.values():
            player.new_round(self.MINIMUM_BET)

        # all players must reset *before* drawing cards, otherwise first player hitting can erroneously proc downstream logic
        for player in self.players.values():
            player.add_hand(Hand(blackjack_max=self.BLACKJACK_MAX))
            self.hit(player, 0)
        for player in self.players.values():
            self.hit(player, 0)
        self.game_exists = True

    def hit(self, player: Player, hand_index: int) -> None:
        current_hand = player.get_hand(hand_index)
        current_hand.hit(self.deck.cards.pop())
        if self._if_all_hands_have_stayed():
            self._resolve_dealer_turn(self.dealer)

    def stay(self, player: Player, hand_index: int) -> None:
        player.stay_hand(hand_index)

        if self._if_all_hands_have_stayed():
            self._resolve_dealer_turn(self.dealer)

    def double_down(self, player: Player, hand_index: int) -> None:
        current_hand = player.get_hand(hand_index)
        current_hand.bet *= self.DOUBLE_DOWN_RATIO
        current_hand.stay()
        self.hit(player, hand_index)

    def split_pair(self, player: Player, hand_index: int) -> None:
        """
        A split is allowed when the player's initial two cards are of the same rank (e.g., two 8s, two Kings).
        The player splits the pair into two separate hands by matching their original bet on the second hand.
        Each hand is then played independently.
        Re-splitting: Some casinos allow players to re-split pairs up to 3-4 times.
        Aces: Splitting Aces usually comes with restrictions, like only one additional card dealt per hand.
        Making 21 after splitting pairs is usually NOT considered a blackjack.
        Doubling after Split (DAS): Some casinos allow doubling down after splitting pairs.
        """
        pass

    # TODO: implement insurance
    def insurance(self, player: Player):
        """
        Insurance is offered when the dealer's upcard is an Ace.
        The player can make a side bet of up to half the original bet that the dealer’s hole card is a 10-value card (making blackjack).
        If the dealer has blackjack, the insurance bet pays 2:1, covering the original bet.
        If the dealer does not have blackjack, the insurance bet is lost.
        """
        pass

    # TODO: implement surrender
    def surrender(self, player: Player):
        """
        The player forfeits half of their original bet and ends their hand immediately.
        Two variants, early surrender and late surrender.
        Early Surrender: Players can surrender before the dealer checks for blackjack. This is less common and generally more favorable to the player.
        Late Surrender: Players can surrender after the dealer checks for blackjack. If the dealer has blackjack, the surrender option is not available.
        """
        pass

    def get_player(self, user_id: str) -> Optional[Player]:
        try:
            return self.players.get(UUID(user_id))
        except Exception as e:
            print(f"Unexpected error when searching for player with user_id {user_id}: {e}")

    def _resolve_dealer_turn(self, dealer: Hand) -> None:
        if dealer.cards[0].hidden:
            dealer.cards[0].flip()

        # dealer draws
        while dealer.sum < BlackjackModel.DEALER_HOLD_THRESHOLD:
            dealer.cards.append(self.deck.cards.pop())

        # evaluate each hand and resolve bets
        for player in self.players.values():
            for hand in player.hands:
                hand.evaluate_outcome(self._determine_outcome(self.dealer.sum, hand.sum, self.dealer.has_blackjack,
                                                              hand.has_blackjack))
            player.evaluate_round_end()

    def _if_all_hands_have_stayed(self) -> bool:
        for player in self.players.values():
            for hand in player.hands:
                if not hand.has_stayed:
                    return False
        return True

    # Todo: determine payouts!
    # Blackjack Payout: 3:2 (e.g., $10 bet wins $15). Some casinos offer 6:5, which is less favorable.
    def _determine_payout(self, player: Player):
        return player.bet

    @staticmethod
    def _determine_outcome(dealer_sum: int, hand_sum: int, dealer_blackjack: bool = False,
                           hand_blackjack: bool = False) -> HandOutcome:
        if hand_sum > BlackjackModel.BLACKJACK_MAX:
            return HandOutcome.LOSE
        elif dealer_sum > BlackjackModel.BLACKJACK_MAX:
            return HandOutcome.WIN
        elif dealer_sum == hand_sum and dealer_blackjack and not hand_blackjack:
            return HandOutcome.LOSE
        elif dealer_sum == hand_sum and hand_blackjack and not dealer_blackjack:
            return HandOutcome.WIN
        elif dealer_sum == hand_sum and hand_blackjack == dealer_blackjack:
            return HandOutcome.PUSH
        elif hand_sum > dealer_sum:
            return HandOutcome.WIN
        elif dealer_sum > hand_sum:
            return HandOutcome.LOSE

    @staticmethod
    def _if_player_wins(player_sum: int, player_blackjack: bool, dealer_sum: int, dealer_blackjack: bool) -> bool:
        if player_sum > BlackjackModel.BLACKJACK_MAX:
            return False
        elif dealer_sum > BlackjackModel.BLACKJACK_MAX:
            return True
        elif player_sum > dealer_sum:
            return True
        elif player_sum == dealer_sum and player_blackjack and not dealer_blackjack:
            return True
        else:
            return False

    @staticmethod
    def _if_player_pushes(player_sum: int, player_blackjack: bool, dealer_sum: int,
                          dealer_blackjack: bool) -> bool:
        return player_sum == dealer_sum and player_blackjack == dealer_blackjack

    @staticmethod
    def get_blackjack_max():
        return BlackjackModel.BLACKJACK_MAX
