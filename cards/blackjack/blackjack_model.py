from typing import List, Dict, Optional
from uuid import UUID, uuid4

from cards.blackjack.player_model import Player
from cards.blackjack.card_model import Card
from cards.blackjack.deck_model import Deck


class BlackjackModel:
    BLACKJACK_MAX = 21
    DEALER_HOLD_THRESHOLD = 17

    def __init__(self):
        self.BET = 50
        self.dealer_sum = None
        self.dealer_cards = None
        self.dealer_blackjack = False
        self.deck = Deck()
        self.game_exists: bool = False
        self.players: Dict[UUID, Player] = {
            player.user_id: player for player in
            [
                Player(player_name='Taylor'),
                Player(player_name='Nate'),
                Player(player_name='Travis')
            ]
        }

    def start_new_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer_blackjack = False
        self.dealer_cards = [Card('0', 'None', hidden=True), self.deck.cards.pop()]
        self.dealer_sum = self.calculate_blackjack_sum(self.dealer_cards)
        for player in self.players.values():
            player.has_stayed = False
            player.has_blackjack = False
            player.has_bust = False
            player.win_or_lose_message = None
            player.hand = []
        # all players must reset before drawing cards, otherwise all players has_stayed will persist for first players hit
        for player in self.players.values():
            self.hit(player)
            self.hit(player)
        self.game_exists = True
        return

    def hit(self, player: Player):
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

    def stay(self, player: Player):
        player.has_stayed = True

        if self.if_all_players_have_stayed():
            self.resolve_dealer_turn()

    def if_all_players_have_stayed(self) -> bool:
        for player in self.players.values():
            if not player.has_stayed:
                return False
        return True

    def player_wins(self, player: Player) -> None:
        player.coins += self.determine_payout(player)
        player.win_or_lose_message = f'You win! +{self.BET} coins!'

    # # Blackjack Payout: 3:2 (e.g., $10 bet wins $15). Some casinos offer 6:5, which is less favorable.
    def determine_payout(self, player: Player):
        return self.BET

    def player_pushes(self, player: Player) -> None:
        player.win_or_lose_message = f'You Push!'

    def player_loses(self, player: Player) -> None:
        player.coins -= self.BET
        player.win_or_lose_message = f'You lose! -{self.BET} coins!'

    def player_busts(self, player: Player) -> None:
        player.win_or_lose_message = f'Busted!'

    # TODO: implement splitting pairs
    def split_pair(self, player: Player):
        pass

    # TODO: implement doubling down
    def double_down(self, player: Player):
        pass

    # TODO: implement insurance
    def insurance(self, player: Player):
        pass

    # TODO: implement surrender
    def surrender(self, player: Player):
        pass

    def has_blackjack(self, player: Player) -> bool:
        return player.sum == BlackjackModel.BLACKJACK_MAX and len(player.hand) == 2

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
            if self.if_player_wins(player.sum, player.has_blackjack, self.dealer_sum, self.dealer_blackjack):
                self.player_wins(player)
            elif self.if_player_pushes(player.sum, player.has_blackjack, self.dealer_sum, self.dealer_blackjack):
                self.player_pushes(player)
            else:
                self.player_loses(player)
        return

    def get_player(self, user_id: str) -> Optional[Player]:
        try:
            return self.players.get(UUID(user_id))
        except Exception as e:
            print(f"Unexpected error when searching for player with {user_id}: {e}")

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

    def if_player_pushes(self, player_sum: int, player_blackjack: bool, dealer_sum: int,
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
