import pytest
from cards.blackjack.card_model import Card


class TestCardModel:
    @pytest.mark.parametrize('rank, suit, hidden, expected_rank, expected_suit', [
        ('A', 'H', False, 'A', 'H'),
        ('K', 'D', False, 'K', 'D'),
        ('10', 'C', False, '10', 'C'),
        ('2', 'S', False, '2', 'S'),
        ('Q', 'H', True, None, None),  # Hidden card returns None
    ])
    def test_card_initialization(self, rank, suit, hidden, expected_rank, expected_suit):
        card = Card(rank, suit, hidden)
        assert card.rank == expected_rank
        assert card.suit == expected_suit
        assert card.hidden == hidden

    def test_card_equality(self):
        card1 = Card('A', 'H')
        card2 = Card('A', 'H')
        card3 = Card('K', 'H')
        card4 = Card('A', 'D')

        assert card1 == card2
        assert card1 != card3
        assert card1 != card4
        assert card3 != card4

    def test_card_equality_with_non_card(self):
        card = Card('A', 'H')
        assert card != "Ace of Hearts"
        assert card != 1
        assert card != None

    @pytest.mark.parametrize('rank, suit, hidden, expected_image', [
        ('A', 'H', False, 'images/playing_cards/A-H.png'),
        ('K', 'D', False, 'images/playing_cards/K-D.png'),
        ('10', 'C', False, 'images/playing_cards/10-C.png'),
        ('2', 'S', True, 'images/playing_cards/BACK.png'),
        ('Q', 'H', True, 'images/playing_cards/BACK.png'),
    ])
    def test_card_image_property(self, rank, suit, hidden, expected_image):
        card = Card(rank, suit, hidden)
        assert card.image == expected_image

    def test_card_flip(self):
        card = Card('A', 'H', hidden=False)
        assert card.hidden is False
        assert card.rank == 'A'
        assert card.suit == 'H'

        card.flip()
        assert card.hidden is True
        assert card.rank is None
        assert card.suit is None

        card.flip()
        assert card.hidden is False
        assert card.rank == 'A'
        assert card.suit == 'H'

    def test_card_hidden_setter(self):
        card = Card('K', 'D', hidden=False)
        assert card.hidden is False

        card.hidden = True
        assert card.hidden is True
        assert card.rank is None
        assert card.suit is None

        card.hidden = False
        assert card.hidden is False
        assert card.rank == 'K'
        assert card.suit == 'D'

    @pytest.mark.parametrize('rank, suit, hidden, expected_dict', [
        ('A', 'H', False, {'rank': 'A', 'suit': 'H', 'image_path': 'images/playing_cards/A-H.png'}),
        ('K', 'D', False, {'rank': 'K', 'suit': 'D', 'image_path': 'images/playing_cards/K-D.png'}),
        ('10', 'C', True, {'rank': None, 'suit': None, 'image_path': 'images/playing_cards/BACK.png'}),
    ])
    def test_card_to_dict(self, rank, suit, hidden, expected_dict):
        card = Card(rank, suit, hidden)
        assert card.to_dict() == expected_dict

    def test_card_rank_property_respects_hidden_state(self):
        card = Card('A', 'H', hidden=False)
        assert card.rank == 'A'

        card.hidden = True
        assert card.rank is None
        assert card._rank == 'A'  # Internal rank still stored

    def test_card_suit_property_respects_hidden_state(self):
        card = Card('K', 'D', hidden=False)
        assert card.suit == 'D'

        card.hidden = True
        assert card.suit is None
        assert card._suit == 'D'  # Internal suit still stored
