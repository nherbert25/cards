// Enum for Hand Outcome
export enum HandOutcome {
    WIN = "WIN",
    LOSE = "LOSE",
    PUSH = "PUSH",
    BLACKJACK = "BLACKJACK",
    BUST = "BUST"
}

// Card Schema
export interface Card {
    rank: string;
    suit: string;
    image_path: string;
}

// Hand Schema
export interface Hand {
    cards: Card[];
    bet: number;
    sum: number;
    has_stayed: boolean;
    has_blackjack: boolean;
    can_split_pair: boolean;
    win_or_lose_message: string;
    outcome: HandOutcome;
}

// Player Schema
export interface Player {
  hands: Hand[];            // Array of cards, where each card is of type 'Card'
  player_name: string;            // Array of cards, where each card is of type 'Card'
  coins: number;              // Bet amount (likely a number)
  bet: number;              // Bet amount (likely a number)
  sum: number;              // Sum of the card values (likely a number)
  has_stayed: boolean;      // Boolean indicating if the player has stayed
  has_blackjack: boolean;   // Boolean indicating if the player has blackjack
  can_split_pair: boolean;  // Boolean indicating if the player can split pairs
  win_or_lose_message: string; // Message about the outcome (Win/Lose/Draw)
  outcome: HandOutcome;     // Outcome of the hand, based on the HandOutcome enum
}

// Dealer Schema
export interface Dealer {
    cards: Card[];
    sum: number;
}

// Blackjack Data Schema
export interface BlackjackData {
    BLACKJACK_MAX: number;
    dealer: Dealer;
    button_counts: {
        button1: number;
        button2: number;
    };
    players: { [player_id: string]: Player };
}
