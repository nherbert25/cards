import pytest
from cards.blackjack.blackjack_model import BlackjackModel, GameConfigs, get_default_players
from cards.blackjack.hand_model import HandOutcome
from cards.blackjack.card_model import Card
from cards.blackjack.deck_model import Deck


class TestGameIntegration:
    """Integration tests that test full game flows"""

    @pytest.fixture
    def game(self, mocker):
        mocker.patch('cards.blackjack.player_model.Player._get_coins_from_db', return_value=500)
        mocker.patch('cards.blackjack.player_model.Player._add_new_user_to_blackjack_table', return_value=None)
        return BlackjackModel(GameConfigs, get_default_players())

    def test_complete_game_flow_player_wins(self, game, mocker):
        """Test complete game where player wins"""
        mocker.patch.object(game.deck, 'shuffle')
        game.start_new_game()

        # Mock coin operations to avoid database calls
        for player in game.players.values():
            mocker.patch.object(player, '_push_coins_to_db', return_value=None)
            mocker.patch.object(player, '_get_coins_from_db', return_value=player.coins)

        player = list(game.players.values())[0]

        # Force a winning scenario: Player has 20, dealer will bust
        player.hands[0].cards = [Card('K', 'H'), Card('Q', 'D')]
        game.dealer.cards = [Card('K', 'C', hidden=True), Card('6', 'S')]

        # Force dealer to bust by ensuring deck has high cards
        game.deck.cards = [Card('K', 'D')] * 10

        # All players stay
        for p in game.players.values():
            game.stay(p, 0)

        # Check that dealer busted and player won
        assert game.dealer.has_bust
        assert player.hands[0].outcome == HandOutcome.WIN

    def test_complete_game_flow_player_loses(self, game, mocker):
        """Test complete game where player loses"""
        mocker.patch.object(game.deck, 'shuffle')
        game.start_new_game()

        # Mock coin operations to avoid database calls
        for player in game.players.values():
            mocker.patch.object(player, '_push_coins_to_db', return_value=None)
            mocker.patch.object(player, '_get_coins_from_db', return_value=player.coins)

        player = list(game.players.values())[0]

        # Force a losing scenario: Player has 18, dealer has 20
        player.hands[0].cards = [Card('9', 'H'), Card('9', 'D')]
        game.dealer.cards = [Card('K', 'C', hidden=True), Card('Q', 'S')]

        # All players stay
        for p in game.players.values():
            game.stay(p, 0)

        # Check outcomes
        assert not game.dealer.has_bust
        assert player.hands[0].outcome == HandOutcome.LOSE

    def test_complete_game_flow_push(self, game, mocker):
        """Test complete game resulting in a push"""
        mocker.patch.object(game.deck, 'shuffle')
        game.start_new_game()

        # Mock coin operations to avoid database calls
        for player in game.players.values():
            mocker.patch.object(player, '_push_coins_to_db', return_value=None)
            mocker.patch.object(player, '_get_coins_from_db', return_value=player.coins)

        player = list(game.players.values())[0]

        # Force a push: Both have 19
        player.hands[0].cards = [Card('K', 'H'), Card('9', 'D')]
        game.dealer.cards = [Card('K', 'C', hidden=True), Card('9', 'S')]

        # Make deck have low cards so dealer doesn't draw
        game.deck.cards = [Card('2', 'D')] * 10

        # All players stay
        for p in game.players.values():
            game.stay(p, 0)

        # Check outcomes
        assert player.hands[0].outcome == HandOutcome.PUSH

    def test_complete_game_flow_player_busts(self, game, mocker):
        """Test game where player busts"""
        mocker.patch.object(game.deck, 'shuffle')
        game.start_new_game()

        player = list(game.players.values())[0]

        # Give player cards that will bust
        player.hands[0].cards = [Card('K', 'H'), Card('Q', 'D')]

        # Hit with a card that causes bust
        game.deck.cards = [Card('K', 'C')] + [Card('2', 'D')] * 50

        game.hit(player, 0)

        # Player should have busted and stayed automatically
        assert player.hands[0].has_bust
        assert player.hands[0].has_stayed

    def test_complete_game_flow_player_gets_blackjack(self, game, mocker):
        """Test game where player gets blackjack"""
        mocker.patch.object(game.deck, 'shuffle')
        game.start_new_game()

        # Mock coin operations to avoid database calls
        for player in game.players.values():
            mocker.patch.object(player, '_push_coins_to_db', return_value=None)
            mocker.patch.object(player, '_get_coins_from_db', return_value=player.coins)

        player = list(game.players.values())[0]

        # Give player blackjack
        player.hands[0].cards = [Card('A', 'H'), Card('K', 'D')]

        # Dealer doesn't have blackjack
        game.dealer.cards = [Card('K', 'C', hidden=True), Card('9', 'S')]

        # All players stay
        for p in game.players.values():
            game.stay(p, 0)

        # Player with blackjack should win
        assert player.hands[0].has_blackjack
        assert player.hands[0].outcome == HandOutcome.WIN

    def test_complete_game_flow_both_blackjack(self, game, mocker):
        """Test game where both player and dealer get blackjack"""
        mocker.patch.object(game.deck, 'shuffle')
        game.start_new_game()

        # Mock coin operations to avoid database calls
        for player in game.players.values():
            mocker.patch.object(player, '_push_coins_to_db', return_value=None)
            mocker.patch.object(player, '_get_coins_from_db', return_value=player.coins)

        player = list(game.players.values())[0]

        # Both have blackjack
        player.hands[0].cards = [Card('A', 'H'), Card('K', 'D')]
        game.dealer.cards = [Card('A', 'C', hidden=True), Card('K', 'S')]

        # All players stay
        for p in game.players.values():
            game.stay(p, 0)

        # Should be a push
        assert player.hands[0].has_blackjack
        assert game.dealer.has_blackjack
        assert player.hands[0].outcome == HandOutcome.PUSH

    def test_complete_game_flow_with_split(self, game, mocker):
        """Test game flow with splitting pairs"""
        mocker.patch.object(game.deck, 'shuffle')
        game.start_new_game()

        player = list(game.players.values())[0]

        # Give player a pair
        player.hands[0].cards = [Card('8', 'H'), Card('8', 'D')]

        # Split the pair
        assert game.split_pair(player, 0)
        assert len(player.hands) == 2

        # Both hands should have received a card
        assert len(player.hands[0].cards) == 2
        assert len(player.hands[1].cards) == 2

    def test_complete_game_flow_with_double_down(self, game, mocker):
        """Test game flow with double down"""
        mocker.patch.object(game.deck, 'shuffle')
        game.start_new_game()

        player = list(game.players.values())[0]
        initial_bet = player.hands[0].bet
        initial_coins = player.coins

        # Double down
        game.double_down(player, 0)

        # Bet should be doubled
        assert player.hands[0].bet == initial_bet * 2

        # Hand should be stayed
        assert player.hands[0].has_stayed

        # Should have received exactly one more card
        assert len(player.hands[0].cards) == 3

    def test_complete_game_multiple_players(self, game, mocker):
        """Test game with multiple players"""
        mocker.patch.object(game.deck, 'shuffle')
        game.start_new_game()

        # Mock coin operations to avoid database calls
        for player in game.players.values():
            mocker.patch.object(player, '_push_coins_to_db', return_value=None)
            mocker.patch.object(player, '_get_coins_from_db', return_value=player.coins)

        # Verify all 3 default players are in game
        assert len(game.players) == 3

        # Each player makes different moves
        players = list(game.players.values())

        # Player 1 hits once then stays
        game.hit(players[0], 0)
        game.stay(players[0], 0)

        # Player 2 stays immediately
        game.stay(players[1], 0)

        # Player 3 hits twice then stays
        game.hit(players[2], 0)
        game.hit(players[2], 0)
        game.stay(players[2], 0)

        # All players should have stayed
        assert all(p.hands[0].has_stayed for p in players)

        # Dealer should have resolved
        assert not game.dealer.cards[0].hidden

    def test_new_game_resets_everything(self, game, mocker):
        """Test that new game properly resets game state"""
        mocker.patch.object(game.deck, 'shuffle')

        # Play a round
        game.start_new_game()
        player = list(game.players.values())[0]
        game.hit(player, 0)
        game.hit(player, 0)

        # Start new game
        game.start_new_game()

        # Everything should be reset
        for player in game.players.values():
            assert len(player.hands) == 1
            assert len(player.hands[0].cards) == 2

        assert len(game.dealer.cards) == 2
        assert game.dealer.cards[0].hidden is True

    def test_coins_update_after_round(self, game, mocker):
        """Test that player coins update correctly after round"""
        mocker.patch.object(game.deck, 'shuffle')
        game.start_new_game()

        player = list(game.players.values())[0]
        initial_coins = player.coins

        # Mock _push_coins_to_db, but mock _get_coins_from_db to return updated value
        bet = player.hands[0].bet
        mocker.patch.object(player, '_push_coins_to_db', return_value=None)
        mocker.patch.object(player, '_get_coins_from_db', return_value=initial_coins + bet)

        # Force a win
        player.hands[0].cards = [Card('K', 'H'), Card('Q', 'D')]  # 20
        game.dealer.cards = [Card('K', 'C', hidden=True), Card('6', 'S')]  # Will draw and likely bust
        game.deck.cards = [Card('K', 'D')] * 10  # Force dealer bust

        # Mock other players
        players = list(game.players.values())
        for p in players[1:]:
            mocker.patch.object(p, '_push_coins_to_db', return_value=None)
            mocker.patch.object(p, '_get_coins_from_db', return_value=p.coins)

        # All players stay
        for p in game.players.values():
            game.stay(p, 0)

        # Player should have won and gained coins
        assert player.coins > initial_coins

    def test_dealer_draws_to_threshold(self, game, mocker):
        """Test that dealer draws cards until reaching threshold"""
        mocker.patch.object(game.deck, 'shuffle')
        game.start_new_game()

        # Mock coin operations to avoid database calls
        for player in game.players.values():
            mocker.patch.object(player, '_push_coins_to_db', return_value=None)
            mocker.patch.object(player, '_get_coins_from_db', return_value=player.coins)

        # Give dealer low cards
        game.dealer.cards = [Card('2', 'C', hidden=True), Card('3', 'S')]

        # Deck has only 5s
        game.deck.cards = [Card('5', 'D')] * 10

        # All players stay
        for p in game.players.values():
            game.stay(p, 0)

        # Dealer should have drawn to at least 17
        assert game.dealer.sum >= BlackjackModel.DEALER_HOLD_THRESHOLD or game.dealer.has_bust
