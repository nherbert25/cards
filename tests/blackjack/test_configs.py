from typing import List

from cards.blackjack.hand_model import Hand, HandOutcome
from cards.blackjack.card_model import Card

initial_game_blackjack = {
    'dealer_cards': [
        {
            'rank': '0',
            'suit': 'None',
            'image_path': 'images/playing_cards/BACK.png'
        },
        {
            'rank': '8',
            'suit': 'S',
            'image_path': 'images/playing_cards/8-S.png '
        }
    ],
    'dealer_sum': 8,
    'button1_count': 0,
    'button2_count': 0,
    'players_data_object': {
        '2290c4b3-5f33-498b-85f1-92da8da356b1': {
            'user_id': '2290c4b3-5f33-498b-85f1-92da8da356b1',
            'sum': 9,
            'hand': [
                {
                    'rank': '3',
                    'suit': 'H',
                    'image_path': 'images/playing_cards/3-H.png '
                },
                {
                    'rank': '6',
                    'suit': 'D',
                    'image_path': 'images/playing_cards/6-D.png '
                }
            ],
            'coins': 500,
            'player_name': 'Taylor',
            'has_stayed': False,
            'win_or_lose_message': None
        },
        'abfd4190-36ac-4eeb-ab17-8e3014f5def0': {
            'user_id': 'abfd4190-36ac-4eeb-ab17-8e3014f5def0',
            'sum': 21,
            'hand': [
                {
                    'rank': 'A',
                    'suit': 'D',
                    'image_path': 'images/playing_cards/A-D.png '
                },
                {
                    'rank': 'K',
                    'suit': 'H',
                    'image_path': 'images/playing_cards/K-H.png '
                }
            ],
            'coins': 500,
            'player_name': 'Nate',
            'has_stayed': False,
            'win_or_lose_message': None
        },
        'd6a41d5a-e06d-4cc0-af4a-78855381ac4b': {
            'user_id': 'd6a41d5a-e06d-4cc0-af4a-78855381ac4b',
            'sum': 12,
            'hand': [
                {
                    'rank': '2',
                    'suit': 'D',
                    'image_path': 'images/playing_cards/2-D.png '
                },
                {
                    'rank': '10',
                    'suit': 'S',
                    'image_path': 'images/playing_cards/10-S.png '
                }
            ],
            'coins': 500,
            'player_name': 'Travis',
            'has_stayed': False,
            'win_or_lose_message': None
        }
    }
}


def generate_test_hand(cards: List[Card]):
    test_hand = Hand()

    for card in cards:
        test_hand.draw_card(card)

    return test_hand


example_hand_total_6 = generate_test_hand([Card('3', 'C'), Card('3', 'C')])
example_hand_total_25 = generate_test_hand([Card('5', 'C'), Card('K', 'C'), Card('Q', 'C')])
