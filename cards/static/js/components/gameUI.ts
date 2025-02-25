// TODO: get the import { io } to work and remove from html
//  import { io } from "https://cdn.socket.io/4.7.4/socket.io.esm.min.js";
//  import { io } from 'socket.io-client';
declare const io: any;
const socket = io();


// gameUI.ts
import {BlackjackData, Card, Hand, Player, Dealer, HandOutcome} from "./schemas";

export function initializeGame() {
    // Set up UI elements, initial state, and event listeners
    const gameContainer = document.getElementById('game-container');
    // Initialize UI here...
}

export function updateUI(state: any) {
    // Modify DOM elements based on the game state
    const playerHand = document.getElementById('player-hand');
    const dealerHand = document.getElementById('dealer-hand');
    const scoreBoard = document.getElementById('score-board');

    // Update the player hand, dealer hand, score, etc.
}










export function updatePageData(data: BlackjackData) {
    console.log("Running UpdatePageData with following data: ");
    console.dir(data);

    const {BLACKJACK_MAX, dealer, button_counts, players} = data;
    console.log("🎲 Blackjack Max:", BLACKJACK_MAX);
    console.log("🃏 Dealer Cards:", dealer.cards);
    console.log("🔘 Button Counts:", button_counts);
    console.log("👥 Players:", Object.keys(players));

    for (const [key, value] of Object.entries(data)) {

        // replaces python syntax with html syntax. Ex: 'your_coins' to 'your-coins'
        const htmlKey = key.replace(/_/g, '-')

        // Update dealer data
        if (htmlKey === "dealer") {
            const {cards, sum} = value;
            updateDealerDiv(cards, sum);
        }

        // Update player data
        if (htmlKey === "players") {
            for (const [playerID, player_data] of Object.entries(value as Record<string, Player>)) {
                updatePlayerDiv(playerID, player_data, BLACKJACK_MAX);
            }
        }

        // Update button counts
        if (htmlKey === "button-counts") {
            const {button1, button2} = value;
            document.getElementById('button1-count')!.innerText = button1;
            document.getElementById('button2-count')!.innerText = button2;
        }
    }
};



export function updateDealerDiv(cards: Card[], sum: number) {
    console.log("Running updateDealerDiv with: ", sum, cards);

    const dealer_sum_element = document.getElementById('dealer-sum')!;
    dealer_sum_element.innerText = sum.toString()

    // Update card images
    const dealer_cards_element = document.getElementById('dealer-cards')!;
    dealer_cards_element.innerHTML = generateCardImages(cards)
};




export function updatePlayerDiv(playerID: string, player_data: Player, BLACKJACK_MAX: number) {
    for (const [key, value] of Object.entries(player_data)) {

        // replaces python syntax with html syntax, then add playerID. Ex: 'player_coins' to 'player-coins-7'
        const htmlKey = key.replace(/_/g, '-') + '-' + playerID

        // grab the corresponding element in the document, if it exists, update the value
        const element = document.getElementById(htmlKey);
        if (element) {
            // TODO: Replace this hard coded 'cards' and 'hand' with a list of all the keys that should have images
            if (htmlKey.includes('cards') || htmlKey.includes('hand')) {
                element.innerHTML = generateCardImages(value)
            } else {
                element.innerText = value;
            }
        }
    }

    // loop through each hand
    for (const [handID, handData] of Object.entries(player_data.hands)) {
        updateHandDiv(playerID, handID, handData, BLACKJACK_MAX)
    }
};

export function updateHandDiv(playerID: string, handID: string, handData: Hand, BLACKJACK_MAX: number): void {
    console.log("Running updateHandDiv with:");
    console.log(playerID, handID, handData);

    // Update header
    const sum: HTMLElement = document.getElementById('sum-' + playerID + '-' + handID)!;
    const message: HTMLElement | null = document.getElementById('win-or-lose-message-' + playerID + '-' + handID)!;

    sum.innerText = handData.sum.toString()
    message.innerHTML = handData.win_or_lose_message

    // Update card images
    const hand_element = document.getElementById('hand-images-' + playerID + '-' + handID)!;
    hand_element.innerHTML = generateCardImages(handData.cards)

    // Update buttons
    const hit_button = document.getElementById('hit-button-' + playerID + '-' + handID) as HTMLButtonElement;
    if (handData.sum > BLACKJACK_MAX || handData.has_stayed) {
        hit_button.disabled = true;
    } else {
        hit_button.disabled = false;
    }

    const stay_button = document.getElementById('stay-button-' + playerID + '-' + handID) as HTMLButtonElement;
    if (handData.sum > BLACKJACK_MAX || handData.has_stayed) {
        stay_button.disabled = true;
    } else {
        stay_button.disabled = false;
    }

    const double_down_button = document.getElementById('double-down-button-' + playerID + '-' + handID) as HTMLButtonElement;
    if (handData.sum > BLACKJACK_MAX || handData.has_stayed) {
        double_down_button.disabled = true;
    } else {
        double_down_button.disabled = false;
    }

    const split_pair_button = document.getElementById('split-pair-button-' + playerID + '-' + handID) as HTMLButtonElement;
    if (!handData.can_split_pair || handData.has_stayed) {
        split_pair_button.disabled = true;
    } else {
        split_pair_button.disabled = false;
    }
};

export function createPlayerDiv(playerID: string, playerData: Player) {
    console.log("Debugging createPlayerDiv playerData:");
    console.dir(playerData);

    const div = document.createElement('div');
    div.className = 'col player';
    div.id = `player-${playerID}`;
    div.innerHTML = `
        <h2 class="player-header">
            <span id="player-name-${playerID}" class="player-name">${playerData.player_name}</span>: 
            <br>
            Coins: <span id="coins-${playerID}" class="player-coins">${playerData.coins}</span>
            <br>
        </h2>
    `;

    // Loop through each hand and create a hand div
    playerData.hands.forEach((handData: Hand, index: number) => {
        const handDiv = createHandDiv(playerID, index.toString(), playerData, handData);
        div.appendChild(handDiv);
    });

    return div;
};

export function createHandDiv(playerID: string, handID: string, playerData: Player, handData: Hand) {
    console.log("Running createHandDiv with:");
    console.dir(playerData);
    console.dir(handData);

    const div = document.createElement('div');
    div.className = 'col hand';
    div.id = `hand-${playerID}-${handID}`;
    div.innerHTML = `
        <span id="win-or-lose-message-${playerID}-${handID}" class="win-or-lose-message">${handData.win_or_lose_message}</span>
        <br>
        Sum: <span id="sum-${playerID}-${handID}" class="hand-sum">${handData.sum}</span> 

<!--        creates hand div for holding cards-->
        <div id="hand-images-${playerID}-${handID}"></div>
<!--        creates button div for holding buttons-->
        <div id="hand-buttons-${playerID}-${handID}" class="hand-buttons">
            <button id='hit-button-${playerID}-${handID}' class="hand-button" onclick="pressHit('${playerID}', ${handID})">Hit</button>
            <button id='stay-button-${playerID}-${handID}' class="hand-button" onclick="pressStay('${playerID}', ${handID})">Stay</button>
            <button id='double-down-button-${playerID}-${handID}' class="hand-button" onclick="pressDoubleDown('${playerID}', ${handID})">Double Down</button>
            <button id='split-pair-button-${playerID}-${handID}' class="hand-button" onclick="pressSplitPair('${playerID}', ${handID})">Split Pair</button>
            <button id='new-game-button-${playerID}-${handID}' class="hand-button" onclick="pressNewGame()">New Game</button>
        </div>
    `;
    return div;
}



function generateCardImages(cards: Card[]) {
    return cards.map(card => `<img src="/static/${card.image_path}" alt="${card.rank} of ${card.suit}" width="125" height="182">`).join('');
};




export async function initializePlayerDivs() {
    try {
        const data = await requestGameData();
        console.log("Attempting to create player divs");
        const playerContainer = document.getElementById('player-container')!;

        playerContainer.innerHTML = '';

        const playersData = data.players;
        for (const [playerID, playerData] of Object.entries(playersData)) {
            const playerDiv = createPlayerDiv(playerID, playerData);
            playerContainer.appendChild(playerDiv);
        }
    } catch (error) {
        console.error('Failed to fetch game data:', error);
    }
}






export function requestGameDataPromise(): Promise<BlackjackData> {
    return new Promise((resolve, reject) => {
        socket.on('request_game_data', function (data: BlackjackData) {
            console.log("request_game_data returned the following data:");
            console.dir(data);
            resolve(data);
        });

        socket.on('request_game_data_error', function (error: any) {
            reject(error);
        });
    });
}

export async function requestGameData(): Promise<BlackjackData> {
    try {
        socket.emit('request_game_data');
        const gameData = await requestGameDataPromise();
        return gameData;
    } catch (error) {
        console.error('Error requesting game data:', error);
        throw error;
    }
}