// https://www.youtube.com/watch?v=4K33w-0-p2c   good video on xml http requests  (callbacks?)
// https://www.youtube.com/watch?v=23hrM4saaMk    rebuilding the last video with the fetch api instead (it's more modern)
// look up async/await. I *think* they're built on top of promises. They're a wrapper that makes the code more readable, yet under the hood they're still promises.
// from my 1 second google, you still write your promise, then your other function will be defined as an async function by adding it as a keyword
// in the definition, aka: "async function myFunction() { ...my code ..  await myPromise() ... my code ..  }"
// https://www.youtube.com/watch?v=AMp6hlA8xKA   using websockets instead of fetch and callbacks

const socket = io();

// after the DOM has loaded, register the following event listeners
document.addEventListener('DOMContentLoaded', async (event) => {
    await initializePlayerDivs();
    generateDebuggerElement();
    refresh_data();
    initializeOnConnectionListener();
    initializeUpdatePageListener();
    initializePlayerJoinListener();
    initializePlayerAddedHandListener();
    initializeButtonCountsListener();
    initializeNewGameListener()
    console.log("DOM fully loaded.");
});

function initializeOnConnectionListener() {
    socket.on('connect', function () {
        console.log('Connected to server');
    })
}

function initializePlayerJoinListener() {
    socket.on('player_joined', function (data) {
        const playerDiv = createPlayerDiv(data.player_name, data.game_data);
        document.getElementById('player-container').appendChild(playerDiv);
    });
}

function initializeNewGameListener() {
    socket.on('initialize_new_game', function (data) {
        try {

            console.log("Client executing initialize_new_game with: ", data);

            // reset and repopulate player-container
            const playerContainer = document.getElementById('player-container');
            playerContainer.innerHTML = '';

            const playersData = data.players;
            for (const [playerID, playerData] of Object.entries(playersData)) {
                const playerDiv = createPlayerDiv(playerID, playerData);
                playerContainer.appendChild(playerDiv);
            }

            // start a new game
            updatePageData(data);

        } catch (error) {
            console.error('Failed to fetch game data:', error);
        }
    });
}


function initializePlayerAddedHandListener() {
    socket.on('player_added_hand', function (data) {
        console.log("Running player_added_hand with: ", data);
        const {player_id, player_data} = data;
        const existingPlayerDiv = document.getElementById('player-' + player_id);
        // TODO: need to create new hand dynamically, currently setting the hand-id to 1 which will break
        //  if hand already exists
        const newHandDiv = createHandDiv(player_id, 1, player_data, player_data.hands[1]);
        existingPlayerDiv.appendChild(newHandDiv);
    });
}

function initializeButtonCountsListener() {
    socket.on('update_button_counts', function (data) {
        // Handle button count updates for the selected game
        document.getElementById('button1-count').innerText = data.counts.button1;
        document.getElementById('button2-count').innerText = data.counts.button2;
    });
}

function initializeUpdatePageListener() {
    socket.on('update_page_data', updatePageData)
};

function updatePageData(data) {
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
            for (const [playerID, player_data] of Object.entries(value)) {
                updatePlayerDiv(playerID, player_data, BLACKJACK_MAX);
            }
        }

        // Update button counts
        if (htmlKey === "button-counts") {
            const {button1, button2} = value;
            document.getElementById('button1-count').innerText = button1;
            document.getElementById('button2-count').innerText = button2;
        }
    }
};

function pressSocketTestingButtons(buttonNumber) {
    socket.emit('press_socket_testing_buttons', {'buttonNumber': buttonNumber});
};

function pressHit(user_id, hand_index = 0) {
    socket.emit('hit', user_id, hand_index);
};

function pressStay(user_id, hand_index = 0) {
    socket.emit('stay', user_id, hand_index);
};

function pressDoubleDown(user_id, hand_index = 0) {
    socket.emit('double_down', user_id, hand_index);
};

function pressSplitPair(user_id, hand_index = 0) {
    socket.emit('split_pair', user_id, hand_index);
};

function pressNewGame() {
    socket.emit('new_game');
};

function refresh_data() {
    socket.emit('update_page_data');
    console.log('Asking server to refresh');
};

function generateCardImages(cards) {
    return cards.map(card => `<img src="/static/${card.image_path}" alt="${card.rank} of ${card.suit}" width="125" height="182">`).join('');
};

function updateDealerDiv(cards, sum) {
    console.log("Running updateDealerDiv with: ", sum, cards);

    const dealer_sum_element = document.getElementById('dealer-sum');
    dealer_sum_element.innerText = sum

    // Update card images
    const dealer_cards_element = document.getElementById('dealer-cards');
    dealer_cards_element.innerHTML = generateCardImages(cards)
};


function updatePlayerDiv(playerID, player_data, BLACKJACK_MAX) {
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

function updateHandDiv(playerID, handID, handData, BLACKJACK_MAX) {
    console.log("Running updateHandDiv with:");
    console.log(playerID, handID, handData);

    // Update header
    const sum = document.getElementById('sum-' + playerID + '-' + handID);
    const message = document.getElementById('win-or-lose-message-' + playerID + '-' + handID);

    sum.innerHTML = handData.sum
    message.innerHTML = handData.win_or_lose_message

    // Update card images
    const hand_element = document.getElementById('hand-images-' + playerID + '-' + handID);
    hand_element.innerHTML = generateCardImages(handData.cards)

    // Update buttons
    const hit_button = document.getElementById('hit-button-' + playerID + '-' + handID);
    if (handData.sum > BLACKJACK_MAX || handData.has_stayed) {
        hit_button.disabled = true;
    } else {
        hit_button.disabled = false;
    }

    const stay_button = document.getElementById('stay-button-' + playerID + '-' + handID);
    if (handData.sum > BLACKJACK_MAX || handData.has_stayed) {
        stay_button.disabled = true;
    } else {
        stay_button.disabled = false;
    }

    const double_down_button = document.getElementById('double-down-button-' + playerID + '-' + handID);
    if (handData.sum > BLACKJACK_MAX || handData.has_stayed) {
        double_down_button.disabled = true;
    } else {
        double_down_button.disabled = false;
    }

    const split_pair_button = document.getElementById('split-pair-button-' + playerID + '-' + handID);
    if (!handData.can_split_pair || handData.has_stayed) {
        split_pair_button.disabled = true;
    } else {
        split_pair_button.disabled = false;
    }
};

function createPlayerDiv(playerID, playerData) {
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
    playerData.hands.forEach((handData, index) => {
        const handDiv = createHandDiv(playerID, index, playerData, handData);
        div.appendChild(handDiv);
    });

    return div;
};

function createHandDiv(playerID, handID, playerData, handData) {
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

function createSocketButtonTestingDiv() {
    console.log("Creating Socket Testing Div");

    const div = document.createElement('div');
    div.className = 'col socket-button-testing';
    div.id = 'socket-button-testing';
    div.innerHTML = `
                <p><b>Debugger: </b></p>
                <button id='socket-debugger-button-1' onclick="pressSocketTestingButtons(1)">Button 1</button>
                <button id='socket-debugger-button-2' onclick="pressSocketTestingButtons(2)">Button 2</button>
                <button id='socket-debugger-refresh-data' onclick="refresh_data()">Refresh Data</button>
                <p>Button 1 Presses: <span id="button1-count">0</span></p>
                <p>Button 2 Presses: <span id="button2-count">0</span></p>
    `;
    return div;
}

function requestGameDataPromise() {
    return new Promise((resolve, reject) => {
        socket.on('request_game_data', function (data) {
            console.log("request_game_data returned the following data:");
            console.dir(data);
            resolve(data);
        });

        socket.on('request_game_data_error', function (error) {
            reject(error);
        });
    });
}

async function requestGameData() {
    try {
        socket.emit('request_game_data');
        const gameData = await requestGameDataPromise();
        return gameData;
    } catch (error) {
        console.error('Error requesting game data:', error);
        throw error;
    }
}

async function initializePlayerDivs() {
    try {
        const data = await requestGameData();
        console.log("Attempting to create player divs");
        const playerContainer = document.getElementById('player-container');

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

// TODO: only call this function if FLASK_ENV=development
function generateDebuggerElement() {
    try {
        const socketTestingContainer = document.getElementById('socket-button-testing-container');
        socketTestingContainer.appendChild(createSocketButtonTestingDiv());
    } catch (error) {
        console.error('generateDebuggerElement error:', error);
    }
}
