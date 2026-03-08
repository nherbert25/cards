import pytest
from cards.blackjack.hand_model import Hand, HandOutcome
from cards.blackjack.card_model import Card


class TestHandModelAdvanced:
    def test_hand_initialization_defaults(self):
        hand = Hand()
        assert hand.cards == []
        assert hand.bet == 50
        assert hand.BLACKJACK_MAX == 21
        assert hand.has_stayed is False
        assert hand.outcome == HandOutcome.NOT_EVALUATED

    def test_hand_initialization_with_cards(self):
        cards = [Card('K', 'H'), Card('Q', 'D')]
        hand = Hand(cards=cards)
        assert len(hand.cards) == 2
        assert hand.sum == 20

    def test_hand_initialization_with_custom_bet(self):
        hand = Hand(bet=100)
        assert hand.bet == 100

    def test_hand_getitem_access(self):
        cards = [Card('K', 'H'), Card('Q', 'D')]
        hand = Hand(cards=cards)
        assert hand[0].rank == 'K'
        assert hand[1].rank == 'Q'

    def test_bet_setter_valid(self):
        hand = Hand()
        hand.bet = 200
        assert hand.bet == 200

    def test_bet_setter_negative_raises_error(self):
        hand = Hand()
        with pytest.raises(ValueError, match="Bet cannot be negative"):
            hand.bet = -50

    def test_has_stayed_auto_true_when_sum_21(self):
        cards = [Card('K', 'H'), Card('A', 'D')]
        hand = Hand(cards=cards)
        assert hand.sum == 21
        assert hand.has_stayed is True

    def test_has_stayed_auto_true_when_sum_over_21(self):
        cards = [Card('K', 'H'), Card('Q', 'D'), Card('5', 'C')]
        hand = Hand(cards=cards)
        assert hand.sum == 25
        assert hand.has_stayed is True

    def test_has_bust_true_when_over_21(self):
        cards = [Card('K', 'H'), Card('Q', 'D'), Card('5', 'C')]
        hand = Hand(cards=cards)
        assert hand.has_bust is True

    def test_has_bust_false_when_21_or_under(self):
        cards = [Card('K', 'H'), Card('Q', 'D')]
        hand = Hand(cards=cards)
        assert hand.has_bust is False

    def test_has_blackjack_true_for_ace_and_ten(self):
        cards = [Card('A', 'H'), Card('K', 'D')]
        hand = Hand(cards=cards)
        assert hand.has_blackjack is True

    def test_has_blackjack_false_for_21_with_three_cards(self):
        cards = [Card('7', 'H'), Card('7', 'D'), Card('7', 'C')]
        hand = Hand(cards=cards)
        assert hand.sum == 21
        assert hand.has_blackjack is False

    def test_can_split_pair_true_for_same_rank(self):
        cards = [Card('8', 'H'), Card('8', 'D')]
        hand = Hand(cards=cards)
        assert hand.can_split_pair is True

    def test_can_split_pair_false_for_different_rank(self):
        cards = [Card('K', 'H'), Card('Q', 'D')]
        hand = Hand(cards=cards)
        assert hand.can_split_pair is False

    def test_can_split_pair_false_with_three_cards(self):
        cards = [Card('8', 'H'), Card('8', 'D'), Card('8', 'C')]
        hand = Hand(cards=cards)
        assert hand.can_split_pair is False

    def test_hit_adds_card_to_hand(self):
        hand = Hand()
        card = Card('K', 'H')
        hand.hit(card)
        assert len(hand.cards) == 1
        assert hand.cards[0] == card

    def test_hit_triggers_bust_message_when_over_21(self):
        cards = [Card('K', 'H'), Card('Q', 'D')]
        hand = Hand(cards=cards)
        hand.hit(Card('5', 'C'))
        assert hand.has_bust is True
        assert hand.win_or_lose_message == 'Busted!'

    def test_hit_triggers_blackjack_message(self):
        cards = [Card('A', 'H')]
        hand = Hand(cards=cards)
        hand.hit(Card('K', 'D'))
        assert hand.has_blackjack is True
        assert hand.win_or_lose_message == 'Blackjack!'

    def test_stay_sets_has_stayed_flag(self):
        hand = Hand()
        assert hand.has_stayed is False
        hand.stay()
        assert hand.has_stayed is True

    def test_split_pair_returns_none_for_invalid_pair(self):
        cards = [Card('K', 'H'), Card('Q', 'D')]
        hand = Hand(cards=cards)
        result = hand.split_pair()
        assert result is None

    def test_split_pair_creates_two_hands(self):
        cards = [Card('8', 'H'), Card('8', 'D')]
        hand = Hand(cards=cards)
        hand1, hand2 = hand.split_pair()

        assert len(hand1.cards) == 1
        assert len(hand2.cards) == 1
        assert hand1.cards[0].rank == '8'
        assert hand2.cards[0].rank == '8'

    def test_evaluate_outcome_win(self):
        hand = Hand()
        hand.evaluate_outcome(HandOutcome.WIN)
        assert hand.outcome == HandOutcome.WIN
        assert 'win' in hand.win_or_lose_message.lower()

    def test_evaluate_outcome_lose(self):
        hand = Hand()
        hand.evaluate_outcome(HandOutcome.LOSE)
        assert hand.outcome == HandOutcome.LOSE
        assert 'lose' in hand.win_or_lose_message.lower()

    def test_evaluate_outcome_push(self):
        hand = Hand()
        hand.evaluate_outcome(HandOutcome.PUSH)
        assert hand.outcome == HandOutcome.PUSH
        assert 'Push' in hand.win_or_lose_message

    def test_draw_card_adds_to_hand(self):
        hand = Hand()
        card = Card('K', 'H')
        hand.draw_card(card)
        assert len(hand.cards) == 1
        assert hand.cards[0] == card

    def test_remove_card_by_index(self):
        cards = [Card('K', 'H'), Card('Q', 'D'), Card('J', 'C')]
        hand = Hand(cards=cards)
        removed = hand.remove_card(index=1)
        assert removed.rank == 'Q'
        assert len(hand.cards) == 2

    def test_remove_card_default_pops_last(self):
        cards = [Card('K', 'H'), Card('Q', 'D'), Card('J', 'C')]
        hand = Hand(cards=cards)
        removed = hand.remove_card()
        assert removed.rank == 'J'
        assert len(hand.cards) == 2

    def test_remove_card_invalid_index_raises_error(self):
        cards = [Card('K', 'H'), Card('Q', 'D')]
        hand = Hand(cards=cards)
        with pytest.raises(IndexError):
            hand.remove_card(index=5)

    def test_get_card_by_index(self):
        cards = [Card('K', 'H'), Card('Q', 'D'), Card('J', 'C')]
        hand = Hand(cards=cards)
        card = hand.get_card(index=1)
        assert card.rank == 'Q'

    def test_get_card_invalid_index_raises_error(self):
        cards = [Card('K', 'H'), Card('Q', 'D')]
        hand = Hand(cards=cards)
        with pytest.raises(IndexError):
            hand.get_card(index=5)

    def test_calculate_blackjack_sum_no_aces(self):
        cards = [Card('K', 'H'), Card('Q', 'D'), Card('5', 'C')]
        assert Hand.calculate_blackjack_sum(cards) == 25

    def test_calculate_blackjack_sum_one_ace_as_11(self):
        cards = [Card('A', 'H'), Card('9', 'D')]
        assert Hand.calculate_blackjack_sum(cards) == 20

    def test_calculate_blackjack_sum_one_ace_as_1(self):
        cards = [Card('A', 'H'), Card('K', 'D'), Card('5', 'C')]
        assert Hand.calculate_blackjack_sum(cards) == 16

    def test_calculate_blackjack_sum_multiple_aces(self):
        cards = [Card('A', 'H'), Card('A', 'D'), Card('A', 'C')]
        assert Hand.calculate_blackjack_sum(cards) == 13

    def test_calculate_blackjack_sum_hidden_card_ignored(self):
        cards = [Card('K', 'H', hidden=True), Card('5', 'D')]
        assert Hand.calculate_blackjack_sum(cards) == 5

    def test_calculate_blackjack_sum_face_cards(self):
        cards = [Card('J', 'H'), Card('Q', 'D'), Card('K', 'C')]
        assert Hand.calculate_blackjack_sum(cards) == 30

    def test_to_dict_contains_all_fields(self):
        cards = [Card('K', 'H'), Card('Q', 'D')]
        hand = Hand(cards=cards, bet=100)
        result = hand.to_dict()

        assert 'cards' in result
        assert 'bet' in result
        assert 'sum' in result
        assert 'has_stayed' in result
        assert 'has_blackjack' in result
        assert 'can_split_pair' in result
        assert 'win_or_lose_message' in result
        assert 'outcome' in result

    def test_to_dict_serializes_cards(self):
        cards = [Card('K', 'H'), Card('Q', 'D')]
        hand = Hand(cards=cards)
        result = hand.to_dict()

        assert len(result['cards']) == 2
        assert result['cards'][0]['rank'] == 'K'
        assert result['cards'][1]['rank'] == 'Q'

    def test_bet_updates_win_or_lose_message(self):
        hand = Hand()
        hand.bet = 100
        assert '100' in hand.win_or_lose_message

    @pytest.mark.parametrize('cards, expected_sum', [
        ([Card('2', 'H'), Card('3', 'D')], 5),
        ([Card('10', 'H'), Card('10', 'D')], 20),
        ([Card('A', 'H'), Card('A', 'D')], 12),
        ([Card('A', 'H'), Card('5', 'D')], 16),
        ([Card('A', 'H'), Card('10', 'D')], 21),
        ([Card('9', 'H'), Card('9', 'D'), Card('3', 'C')], 21),
    ])
    def test_sum_property_various_hands(self, cards, expected_sum):
        hand = Hand(cards=cards)
        assert hand.sum == expected_sum
