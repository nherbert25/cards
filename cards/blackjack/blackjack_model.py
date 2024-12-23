from enum import Enum
from typing import List, Dict, Optional
from uuid import UUID, uuid4

from cards.blackjack.player_model import Player
from cards.blackjack.card_model import Card
from cards.blackjack.deck_model import Deck


class PlayerOutcome(Enum):
    WIN = 'win'
    LOSE = 'lose'
    PUSH = 'push'


class GameConfigs:
    # Game configs:
    NUMBER_OF_DECKS = 1
    BLACKJACK_RATIO = 1.5  # Standard payouts for a blackjack (Ace + 10-value card) are 3:2, but some tables pay 6:5, which increases the house edge.

    # Variants
    DEALER_HITS_ON_SOFT_17 = False  # Dealers must hit on soft 17 (Ace + 6) or stand on all 17s, depending on the casino’s rules. Soft Hand: A hand containing an Ace counted as 11. For example, Ace + 6 = "Soft 17."
    RESTRICTED_DOUBLING = False  # Some tables limit doubling down to totals of 9, 10, or 11.
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

    # TODO: make win, lose and push state an enum since they're not mutually exclusive. Writing them as independent bools is unnecessary and error prone
    # TODO: fix bug where player will push if dealer and player both have 22 !!!

    def __init__(self, game_configs: GameConfigs):
        self.BET = 50
        self.dealer_sum = None
        self.dealer_cards = None
        self.dealer_blackjack = False
        self.deck = Deck()
        self.game_exists: bool = False

        # Unpack the game_configs attributes into the class instance
        self.__dict__.update(game_configs.__dict__)

        self.players: Dict[UUID, Player] = {
            player.user_id: player for player in
            [
                Player(player_name='Taylor', user_id=UUID("11111111-1111-1111-1111-111111111111")),
                Player(player_name='Nate', user_id=UUID("22222222-2222-2222-2222-222222222222")),
                Player(player_name='Travis', user_id=UUID("33333333-3333-3333-3333-333333333333")),
            ]
        }

    def start_new_game(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer_blackjack = False
        self.dealer_cards = [Card('0', 'None', hidden=True), self.deck.cards.pop()]
        self.dealer_sum = self.calculate_blackjack_sum(self.dealer_cards)
        for player in self.players.values():
            player.has_stayed = False
            player.has_blackjack = False
            player.player_outcome = None
            player.win_or_lose_message = None
            player.hand = []
        # all players must reset *before* drawing cards, otherwise has_stayed will have persisted when first players hits
        for player in self.players.values():
            self.hit(player)
            self.hit(player)
        self.game_exists = True

    def hit(self, player: Player) -> None:
        player.draw_card(self.deck.cards.pop())
        player.sum = self.calculate_blackjack_sum(player.hand)
        if player.sum > BlackjackModel.BLACKJACK_MAX:
            player.has_stayed = True
            player.has_bust = True
            self.player_busts(player)

        if player.sum == BlackjackModel.BLACKJACK_MAX:
            if self.has_blackjack(player):
                player.has_blackjack = True
                player.win_or_lose_message = 'Blackjack!'
            self.stay(player)

        if self.if_all_players_have_stayed():
            self.resolve_dealer_turn()

    def stay(self, player: Player) -> None:
        player.has_stayed = True

        if self.if_all_players_have_stayed():
            self.resolve_dealer_turn()

    def if_all_players_have_stayed(self) -> bool:
        for player in self.players.values():
            if not player.has_stayed:
                return False
        return True

    # Todo: determine payouts!
    # Blackjack Payout: 3:2 (e.g., $10 bet wins $15). Some casinos offer 6:5, which is less favorable.
    def determine_payout(self, player: Player):
        return self.BET

    def player_wins(self, player: Player) -> None:
        player.coins += self.determine_payout(player)
        player.win_or_lose_message = f'You win! +{self.BET} coins!'

    def player_pushes(self, player: Player) -> None:
        player.win_or_lose_message = f'You Push!'

    def player_loses(self, player: Player) -> None:
        player.coins -= self.BET
        player.win_or_lose_message = f'You lose! -{self.BET} coins!'

    def player_busts(self, player: Player) -> None:
        player.win_or_lose_message = f'Busted!'

    # TODO: implement splitting pairs
    # A split is allowed when the player's initial two cards are of the same rank (e.g., two 8s, two Kings).
    # The player splits the pair into two separate hands by matching their original bet on the second hand.
    # Each hand is then played independently.
    # Re-splitting: Some casinos allow players to re-split pairs up to 3-4 times.
    # Aces: Splitting Aces usually comes with restrictions, like only one additional card dealt per hand.
    # Doubling after Split (DAS): Some casinos allow doubling down after splitting pairs.
    def split_pair(self, player: Player):
        pass

    # TODO: implement doubling down
    """The player can double down on their initial two-card total. 
    The player doubles their initial bet and commits to receiving only one additional card.
    Some casinos restrict doubling down to certain totals (e.g., only 10 or 11).
    """

    def double_down(self, player: Player):
        pass

    # TODO: implement insurance
    """
    Insurance is offered when the dealer's upcard is an Ace.
    The player can make a side bet of up to half the original bet that the dealer’s hole card is a 10-value card (making blackjack).
    If the dealer has blackjack, the insurance bet pays 2:1, covering the original bet.
    If the dealer does not have blackjack, the insurance bet is lost.
    """

    def insurance(self, player: Player):
        pass

    # TODO: implement surrender
    # The player forfeits half of their original bet and ends their hand immediately.
    # Two variants, early surrender and late surrender.
    # Early Surrender: Players can surrender before the dealer checks for blackjack. This is less common and generally more favorable to the player.
    # Late Surrender: Players can surrender after the dealer checks for blackjack. If the dealer has blackjack, the surrender option is not available.
    def surrender(self, player: Player):
        pass

    def resolve_dealer_turn(self, dealer_cards=None) -> None:
        if dealer_cards is None:
            dealer_cards = self.dealer_cards

        flip_face_down_card = self.deck.cards.pop()
        dealer_cards[0] = flip_face_down_card

        # dealer draws
        self.dealer_sum = self.calculate_blackjack_sum(dealer_cards)
        while self.dealer_sum < BlackjackModel.DEALER_HOLD_THRESHOLD:
            dealer_cards.append(self.deck.cards.pop())
            self.dealer_sum = self.calculate_blackjack_sum(dealer_cards)
            if self.dealer_sum == BlackjackModel.BLACKJACK_MAX and len(dealer_cards) == 2:
                self.dealer_blackjack = True

        # determine winners
        for player in self.players.values():
            player.player_outcome = self.determine_outcome(self.dealer_sum, player.sum, self.dealer_blackjack,
                                                           player.has_blackjack)
            if player.player_outcome == PlayerOutcome.WIN:
                self.player_wins(player)
            elif player.player_outcome == PlayerOutcome.PUSH:
                self.player_pushes(player)
            else:
                self.player_loses(player)
        return

    @staticmethod
    def determine_outcome(dealer_sum: int, player_sum: int, dealer_blackjack: bool = False,
                          player_blackjack: bool = False) -> PlayerOutcome:
        if player_sum > BlackjackModel.BLACKJACK_MAX:
            return PlayerOutcome.LOSE
        elif dealer_sum > BlackjackModel.BLACKJACK_MAX:
            return PlayerOutcome.WIN
        elif dealer_sum == player_sum and dealer_blackjack and not player_blackjack:
            return PlayerOutcome.LOSE
        elif dealer_sum == player_sum and player_blackjack and not dealer_blackjack:
            return PlayerOutcome.WIN
        elif dealer_sum == player_sum and player_blackjack == dealer_blackjack:
            return PlayerOutcome.PUSH
        elif player_sum > dealer_sum:
            return PlayerOutcome.WIN
        elif dealer_sum > player_sum:
            return PlayerOutcome.LOSE

    def get_player(self, user_id: str) -> Optional[Player]:
        try:
            return self.players.get(UUID(user_id))
        except Exception as e:
            print(f"Unexpected error when searching for player with user_id {user_id}: {e}")

    def has_blackjack(self, player: Player) -> bool:
        return player.sum == BlackjackModel.BLACKJACK_MAX and len(player.hand) == 2

    @staticmethod
    def if_player_wins(player_sum: int, player_blackjack: bool, dealer_sum: int, dealer_blackjack: bool) -> bool:
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
    def if_player_pushes(player_sum: int, player_blackjack: bool, dealer_sum: int,
                         dealer_blackjack: bool) -> bool:
        return player_sum == dealer_sum and player_blackjack == dealer_blackjack

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
            if result + 11 > BlackjackModel.BLACKJACK_MAX:
                return result + 1
            else:
                return result + 11
        elif ace_count > 1:
            if result + 11 + ace_count - 1 > BlackjackModel.BLACKJACK_MAX:
                return result + ace_count
            else:
                return result + 11 + ace_count - 1
        return result

    @staticmethod
    def get_blackjack_max():
        return BlackjackModel.BLACKJACK_MAX
