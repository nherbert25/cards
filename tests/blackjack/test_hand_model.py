import pytest

from tests.blackjack.test_configs import example_hand_total_KQ, example_hand_total_KK, example_hand_total_QQQ, \
    generate_test_hand
#     example_hand_KK, example_hand_KQ

from cards.blackjack.hand_model import Hand
from cards.blackjack.card_model import Card


example_hand_total_KQ = generate_test_hand([Card('K', 'C'), Card('Q', 'C')])
example_hand_total_KK = generate_test_hand([Card('K', 'C'), Card('K', 'D')])
example_hand_total_QQQ = generate_test_hand([Card('Q', 'C'), Card('Q', 'D'), Card('Q', 'H')])



# @pytest.mark.parametrize('test_input, expected_output', [
#     (example_hand_total_KQ, False),
#     (example_hand_total_KK, True),
#     (example_hand_total_QQQ, False),
# ])
# def test_can_split_pair(generate_hands, test_input, expected_output):
#     print([(card.rank, card.suit) for card in generate_hands.cards])
#     assert generate_hands.can_split_pair == expected_output



# @pytest.mark.parametrize("hand_key, expected_output", [
#     ("KQ", False),  # Not a pair
#     ("KK", True),   # A pair
#     ("QQQ", False), # Three of a kind
# ])
# def test_can_split_pair(test_hands, hand_key, expected_output):
#     test_hand = test_hands[hand_key]  # Retrieve hand from fixture
#     print("MEOW!!!!: ", [(card.rank, card.suit) for card in test_hand.cards])
#     assert test_hand.can_split_pair == expected_output
#

@pytest.mark.parametrize("hand_name, expected_output", [
    ("KQ", False),
    ("KK", True),
    ("QQQ", False),
    ("5KQ", False),
    ("33", True),
    ("333", False),
])
def test_can_split_pair(hand_factory, hand_name, expected_output):
    test_hand = hand_factory(hand_name)
    assert test_hand.can_split_pair == expected_output

#
#
# @pytest.mark.parametrize('test_input, expected_output', [
#     (example_hand_total_KQ, False),
#     (example_hand_KK, True),
#     (example_hand_total_QQQ, False),
# ]
#                          )
# def test_can_split_pair(example_hand_KK, test_input, expected_output):
#     assert test_input.can_split_pair == expected_output




################################################
################################################
################################################
################################################
################################################
################################################
################################################
################################################
################################################
################################################
################################################
################################################
################################################
################################################
################################################
################################################





class TestHandModel:
    # @pytest.fixture(autouse=True)
    # def mock_game(self, mocker):
    #     self.hand_KK = example_hand_KK()
    #     self.hand_KQ = example_hand_KQ()

    # working test with parametrization (allows you to run the same test with multiple inputs) note that 'test_input,
    # expected_output' is a SINGLE string! also note the class must be instantiated first. pytest methods do not take
    # the 'self' keyword, you must *always* instantiate your test class.
    @pytest.mark.parametrize('test_input, expected_output', [
        ([], 0),
        ([Card('10', 'C')], 10),
        ([Card('3', 'C'), Card('3', 'C')], 6),
        ([Card('5', 'C'), Card('K', 'C'), Card('Q', 'C')], 25),
        ([Card('A', 'C'), Card('A', 'D')], 12),
        ([Card('A', 'C'), Card('A', 'D'), Card('A', 'D')], 13),
        ([Card('A', 'C'), Card('J', 'D')], 21),
        ([Card('A', 'C'), Card('A', 'D'), Card('Q', 'D')], 12)
    ]
                             )
    def test_calculate_blackjack_sum(self, test_input, expected_output):
        model = Hand()
        result = model.calculate_blackjack_sum(test_input)
        assert result == expected_output

    @pytest.mark.parametrize('test_input, expected_output', [
        (example_hand_total_KQ, False),
        (example_hand_total_KK, True),
        (example_hand_total_QQQ, False),
    ]
                             )
    def test_can_split_pair(self, test_input, expected_output):
        assert test_input.can_split_pair == expected_output

    # @pytest.mark.parametrize('test_input, expected_output', (
    #         # (pytest.lazy_fixture(example_hand_KK), (Card('K', 'C'), (Card('K', 'D')))),
    #         (example_hand_KK, (Card('K', 'C'), (Card('K', 'D')))),
    #         (example_hand_KQ, None),
    # ))
    # def test_split_pair(self, test_input, expected_output):
    #     if not test_input.can_split_pair:
    #         assert test_input.split_pair() is None
    #
    #     else:
    #         hand_1, hand_2 = test_input.split_pair()
    #         assert hand_1[0] == expected_output[0]
    #         assert hand_2[0] == expected_output[1]
