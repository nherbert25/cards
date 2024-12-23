// https://www.youtube.com/watch?v=4K33w-0-p2c   good video on xml http requests  (callbacks?)
// https://www.youtube.com/watch?v=23hrM4saaMk    rebuilding the last video with the fetch api instead (it's more modern)
// look up async/await. I *think* they're built on top of promises. They're a wrapper that makes the code more readable, yet under the hood they're still promises.
// from my 1 second google, you still write your promise, then your other function will be defined as an async function by adding it as a keyword
// in the definition, aka: "async function myFunction() { ...my code ..  await myPromise() ... my code ..  }"
// https://www.youtube.com/watch?v=AMp6hlA8xKA   using websockets instead of fetch and callbacks

const socket = io();


document.addEventListener('DOMContentLoaded', async (event) => {
    await initializePlayerDivs();
    generateDebuggerElement();
    refresh_data();
    initializeOnConnectionListener();
    initializeUpdatePageListener();
    initializePlayerJoinListener();
    initializeButtonCountsListener();
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

function initializeButtonCountsListener() {
    socket.on('update_button_counts', function (data) {
        // Handle button count updates for the selected game
        document.getElementById('button1-count').innerText = data.counts.button1;
        document.getElementById('button2-count').innerText = data.counts.button2;
    });
}

function initializeUpdatePageListener() {
    socket.on('update_page_data', function (data) {

        console.log("UpdatePageData returned the following data:");
        console.dir(data);

        for (const [key, value] of Object.entries(data)) {

            // replaces python syntax with html syntax. Ex: 'your_coins' to 'your-coins'
            const htmlKey = key.replace(/_/g, '-')

            if (htmlKey === "players-data-object") {
                for (const [playerID, player_value] of Object.entries(value)) {
                    updatePlayerDiv(playerID, player_value, data.BLACKJACK_MAX);
                }

            } else {
                const element = document.getElementById(htmlKey);
                if (element) {
                    if (htmlKey.includes('cards') || htmlKey.includes('hand')) {
                        element.innerHTML = generateCardImages(value)
                    } else {
                        element.innerText = value;
                    }
                }
            }
        }
    })
};

function pressSocketTestingButtons(buttonNumber) {
    socket.emit('press_socket_testing_buttons', {'buttonNumber': buttonNumber});
};

function pressHit(user_id) {
    socket.emit('hit', user_id);
};

function pressStay(user_id) {
    socket.emit('stay', user_id);
};

function pressDoubleDown(user_id){
    socket.emit('double_down', user_id);
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
}

function updatePlayerDiv(playerID, player_data, BLACKJACK_MAX) {
    for (const [key, value] of Object.entries(player_data)) {

        // replaces python syntax with html syntax, then add playerID. Ex: 'player_coins' to 'player-coins-7'
        const htmlKey = key.replace(/_/g, '-') + '-' + playerID
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

    const hit_button = document.getElementById('hit-button-' + playerID);
    if (player_data.sum > BLACKJACK_MAX || player_data.has_stayed) {
        hit_button.disabled = true;
    } else {
        hit_button.disabled = false;
    }

    const stay_button = document.getElementById('stay-button-' + playerID);
    if (player_data.sum > BLACKJACK_MAX || player_data.has_stayed) {
        stay_button.disabled = true;
    } else {
        stay_button.disabled = false;
    }

    const double_down_button = document.getElementById('double-down-button-' + playerID);
    if (player_data.sum > BLACKJACK_MAX || player_data.has_stayed) {
        double_down_button.disabled = true;
    } else {
        double_down_button.disabled = false;
    }
}

function createPlayerDiv(playerID, playerData) {
    console.log("Debugging createPlayerDiv playerData:");
    console.dir(playerData);

    const div = document.createElement('div');
    div.className = 'col player';
    div.id = `player-${playerID}`;
    div.innerHTML = `
        <h2 class="player-header">
            <span id="player-name-${playerID}" class="player-name">${playerData.player_name}</span>: 
            <span id="sum-${playerID}" class="player-sum">${playerData.sum}</span> 
            <span id="win-or-lose-message-${playerID}" class="win-or-lose-message">${playerData.win_or_lose_message}</span>
            <br>
            Coins: <span id="coins-${playerID}" class="player-coins">${playerData.coins}</span>
            <br>
        </h2>
        <div id="hand-${playerID}" class="player-hand"></div>
        <div class="player-buttons">
            <button id='hit-button-${playerID}' class="player-button" onclick="pressHit('${playerID}')">Hit</button>
            <button id='stay-button-${playerID}' class="player-button" onclick="pressStay('${playerID}')">Stay</button>
            <button id='double-down-button-${playerID}' class="player-button" onclick="pressDoubleDown('${playerID}')">Double Down</button>
            <button id='new-game-button-${playerID}' class="player-button" onclick="pressNewGame()">New Game</button>
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
                <p>Button 1 Presses: <span id="button1-count">{{ button1_count }}</span></p>
                <p>Button 2 Presses: <span id="button2-count">{{ button2_count }}</span></p>
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

        const playersData = data.players_data_object;
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
