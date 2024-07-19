from random import shuffle as r_shuffle
from typing import List
from cards.blackjack.player_model import Player
from cards.blackjack.card_model import Card


class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['S', 'H', 'D', 'C']
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]

    def shuffle(self):
        r_shuffle(self.cards)


class BlackjackModel:
    def __init__(self):
        self.dealer_sum = None
        self.dealer_cards = None
        self.deck = Deck()
        self.game_exists: bool = False
        self.BET = 50
        # todo: turn self.players into a dictionary {1: {user_id:1, player_name:'Taylor'}, etc.} then use self.players.get(player_id). You'll have to restructure controller and js.
        self.players: List[Player] = [Player(1, 'Taylor'), Player(2, 'Nate'), Player(3, 'Travis')]

    def start_new_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer_cards = [Card('0', 'None', hidden=True), self.deck.cards.pop()]
        self.dealer_sum = self.calculate_blackjack_sum(self.dealer_cards)
        for player in self.players:
            player.hand = []
            player.draw_card(self.deck.cards.pop())
            player.draw_card(self.deck.cards.pop())
            player.sum = self.calculate_blackjack_sum(player.hand)
            player.has_stayed = False
            player.win_or_lose_message = None
        self.game_exists = True
        return

    def hit(self, player: Player):
        player.draw_card(self.deck.cards.pop())
        player.sum = self.calculate_blackjack_sum(player.hand)
        if player.sum > 21:
            player.has_stayed = True
        if self.if_all_players_have_stayed():
            self.resolve_dealer_turn()

    def stay(self, player: Player):
        player.has_stayed = True

        if self.if_all_players_have_stayed():
            self.resolve_dealer_turn()

    def if_all_players_have_stayed(self) -> bool:
        for player in self.players:
            if not player.has_stayed:
                return False
        return True

    def if_player_wins(self, player_sum: int, dealer_sum: int) -> bool:
        if player_sum > 21:
            return False
        elif dealer_sum > 21:
            return True
        elif player_sum > dealer_sum:
            return True
        else:
            return False

    def you_win(self, player: Player):
        player.coins += self.BET
        player.win_or_lose_message = f'You win! +{self.BET} coins!'

    def you_lose(self, player: Player):
        player.coins -= self.BET
        player.win_or_lose_message = f'You lose! -{self.BET} coins!'

    def resolve_dealer_turn(self, dealer_cards=None):
        if dealer_cards is None:
            dealer_cards = self.dealer_cards

        flip_face_down_card = self.deck.cards.pop()
        dealer_cards[0] = flip_face_down_card

        self.dealer_sum = self.calculate_blackjack_sum(dealer_cards)
        while self.dealer_sum < 17:
            dealer_cards.append(self.deck.cards.pop())
            self.dealer_sum = self.calculate_blackjack_sum(dealer_cards)
        for player in self.players:
            if self.if_player_wins(player.sum, self.dealer_sum):
                self.you_win(player)
            else:
                self.you_lose(player)
        return

    def get_player(self, user_id):
        try:
            for player in self.players:
                if player.user_id == user_id or player.user_id == int(user_id):
                    return player
        except Exception as e:
            print(f"error: No player with user_id: {user_id} exists\r\n{e}")

    def calculate_blackjack_sum(self, card_list: List[Card]) -> int:
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
            if result + 11 > 21:
                return result + 1
            else:
                return result + 11
        elif ace_count > 1:
            if result + 11 + ace_count - 1 > 21:
                return result + ace_count
            else:
                return result + 11 + ace_count - 1
        return result
