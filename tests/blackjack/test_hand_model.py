import pytest

from cards.blackjack.hand_model import Hand
from cards.blackjack.card_model import Card


class TestHandModel:
    # @pytest.fixture(autouse=True)  #  autouse=True means you do not have to explicitly input the fixture
    # def mock_game(self, mocker):
    #     self.hand_KK = example_hand_KK()
    #     self.hand_KQ = example_hand_KQ()

    @pytest.mark.parametrize('hand_name, expected_output', [
        ("empty_hand", 0),
        ("9", 9),
        ("33", 6),
        ("5KQ", 25),
        ("AA", 12),
        ("AAA", 13),
        ("AJ", 21),
        ("AAQ", 12)
    ])
    def test_calculate_blackjack_sum(self, hand_factory, hand_name, expected_output):
        """Parametrization allows you to run the same test with multiple inputs. Note that 'test_input,
        expected_output' is a SINGLE string! Also note the class must be instantiated first. pytest methods do not take
        the 'self' keyword, you must *always* instantiate your test class."""
        hand_model = Hand()
        test_hand = hand_factory(hand_name)
        result = hand_model.calculate_blackjack_sum(test_hand.cards)
        assert result == expected_output

    @pytest.mark.parametrize("hand_name, expected_output", [
        ("KQ", False),
        ("KK", True),
        ("QQQ", False),
        ("5KQ", False),
        ("33", True),
        ("333", False),
        ("AAQ", False)
    ])
    def test_can_split_pair(self, hand_factory, hand_name, expected_output):
        test_hand = hand_factory(hand_name)
        assert test_hand.can_split_pair == expected_output

    @pytest.mark.parametrize('hand_name, expected_output', [
            ("KK", (Card('K', 'C'), Card('K', 'D'))),
            ("KQ", None),
            ("33", (Card('3', 'C'), Card('3', 'C'))),
            ("333", None),
    ])
    def test_split_pair(self, hand_factory, hand_name, expected_output):
        test_hand = hand_factory(hand_name)
        if not test_hand.can_split_pair:
            assert test_hand.split_pair() is None

        else:
            hand_1, hand_2 = test_hand.split_pair()
            assert hand_1[0] == expected_output[0]
            assert hand_2[0] == expected_output[1]
