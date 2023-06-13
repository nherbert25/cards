import pytest
from black_jack.blackjack_model import Card, BlackjackModel


# example test without parametrization
# def test_calculate_black_jack_sum():
#     result = calculate_black_jack_sum([Card('3', 'C'), Card('3', 'C')])
#     expected_result = 6
#     assert result == expected_result

# TODO: This test is broken after converting function to method
# working test with parametrization (allows you to run the same test with multiple inputs) note that 'test_input,
# expected_output' is a SINGLE string!
@pytest.mark.parametrize('test_input, expected_output', [([], 0),
                                                         ([Card('10', 'C')], 10),
                                                         ([Card('3', 'C'), Card('3', 'C')], 6),
                                                         ([Card('5', 'C'), Card('K', 'C'), Card('Q', 'C')], 25),
                                                         ([Card('A', 'C'), Card('A', 'D')], 12),
                                                         ([Card('A', 'C'), Card('A', 'D'), Card('A', 'D')], 13),
                                                         ([Card('A', 'C'), Card('J', 'D')], 21),
                                                         ([Card('A', 'C'), Card('A', 'D'), Card('Q', 'D')], 12)])
def test_calculate_black_jack_sum(test_input, expected_output):
    result = BlackjackModel.calculate_black_jack_sum(test_input)
    assert result == expected_output
