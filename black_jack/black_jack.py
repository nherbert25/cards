from random import shuffle as r_shuffle


class Card:
    """
    Card class that represents each card in the deck.

    Attributes:
        rank (str): Represents the point value of each card (2 - Ace).
        suit (str): Represents the suit of each card (Hearts, Diamonds, Clubs, Spades).
        image (str): Represents the filepath to each card image that is displayed on the page.

    """

    def __init__(self, rank, suit, image=None):
        self.rank = rank
        self.suit = suit
        self.image = image


class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['S', 'H', 'D', 'C']
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]

    def shuffle(self):
        r_shuffle(self.cards)


def start_new_game():
    deck = Deck()
    deck.shuffle()
    dealer_cards = [deck.cards.pop()]
    dealer_sum = calculate_black_jack_sum(dealer_cards)
    your_cards = [deck.cards.pop(), deck.cards.pop()]
    your_sum = calculate_black_jack_sum(your_cards)
    return deck, dealer_cards, dealer_sum, your_cards, your_sum


# TODO write a test. There's a bug!!! A + A + 10 != 22  !!
def calculate_black_jack_sum(card_list: list[Card]) -> int:
    my_sum = 0
    ace_count = 0
    for card in card_list:
        if card.rank == 'A':
            ace_count += 1
        else:
            if card.rank in ['J', 'Q', 'K']:
                value = 10
            else:
                value = int(card.rank)
            my_sum += value
    for i in range(ace_count):
        if my_sum + 11 > 21:
            my_sum += 1
        else:
            my_sum += 11
    return my_sum


player_name = 'Taylor'
