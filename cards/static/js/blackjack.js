// https://www.youtube.com/watch?v=4K33w-0-p2c   good video on xml http requests  (callbacks?)
// https://www.youtube.com/watch?v=23hrM4saaMk    rebuilding the last video with the fetch api instead (it's more modern)
// look up async/await. I *think* they're built on top of promises. They're a wrapper that makes the code more readable, yet under the hood they're still promises.
// from my 1 second google, you still write your promise, then your other function will be defined as an async function by adding it as a keyword
// in the definition, aka: "async function myFunction() { ...my code ..  await myPromise() ... my code ..  }"
// https://www.youtube.com/watch?v=AMp6hlA8xKA   using websockets instead of fetch and callbacks

const socket = io();


document.addEventListener('DOMContentLoaded', (event) => {
    refresh_data();
    initializeOnConnectionListener();
    // initializeRequestGameDataPromise();
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
        console.log(data.counts);
    });
}

function initializeUpdatePageListener() {
    let pageData;

    socket.on('update_page_data', function (data) {
        // Update HTML elements based on received data

        console.log("UpdatePageData returned the following data:");
        console.dir(data);

        for (const [key, value] of Object.entries(data)) {

            pageData = data;

            // replaces python syntax with html syntax. Ex: 'your_coins' to 'your-coins'
            const htmlKey = key.replace(/_/g, '-')
            const element = document.getElementById(htmlKey);
            if (element) {
                if (htmlKey.includes('cards')) {
                    element.innerHTML = generateCardImages(value)
                } else {
                    element.innerText = value;
                }
            }

            const hit_button = document.getElementById('hit-button');
            if (pageData.your_sum > 21 || pageData.has_stayed) {
                hit_button.disabled = true;
            } else {
                hit_button.disabled = false;
            }

            const stay_button = document.getElementById('stay-button');
            if (pageData.your_sum > 21 || pageData.has_stayed) {
                stay_button.disabled = true;
            } else {
                stay_button.disabled = false;
            }
        }
        console.log('Updating page content: ', data);
    });
}

function pressSocketTestingButtons(buttonNumber) {
    socket.emit('press_socket_testing_buttons', {'buttonNumber': buttonNumber});
};

function pressButtons(buttonName) {
    socket.emit('press_buttons', buttonName);
};

function refresh_data() {
    socket.emit('update_page_data');
    console.log('Asking server to refresh');
};

function generateCardImages(cards) {
    return cards.map(card => `<img src="/static/${card.image_path}" alt="${card.rank} of ${card.suit}" width="125" height="182">`).join('');
}

// TODO: update function by adding "-${playerName}" to all ids. for example: id='hit-button' goes to id='hit-button-${playerName}' once users are implemented
function createPlayerDiv(playerName = 'Taylor', gameData) {
    console.log("Debugging createPlayerDiv gameData:");
    console.dir(gameData)

    const div = document.createElement('div');
    div.className = 'player';
    div.id = `player-${playerName}`;
    div.innerHTML = `
        <h2>${playerName}: <span id="your-sum">${gameData.your_sum}</span> <span id="win-or-lose-message"></span>
            <br>
            Coins: <span id="your-coins">${gameData.your_coins}</span>
            <br>
        </h2>
        <div id="your-cards"></div>
        <button id='hit-button' onclick="pressButtons('hit', '${playerName}')">Hit</button>
        <button id='stay-button' onclick="pressButtons('stay', '${playerName}')">Stay</button>
        <button id='new-game-button' onclick="pressButtons('new_game', '${playerName}')">New Game</button>
    `;
    return div;
}

// todo: refactor this function as this is NOT a normal event listener. This is a generate promise function thing
function initializeRequestGameDataPromise() {
    return new Promise((resolve, reject) => {
        socket.on('request_game_data', function (data) {
            console.log("TESTING TESTING TESTING Returned the following data:");
            console.dir(data);
            resolve(data); // Resolve the promise with the received data
        });

        // Optional: Handle errors if needed
        socket.on('request_game_data_error', function (error) {
            reject(error); // Reject the promise with the error
        });
    });
}

async function requestGameData() {
    try {
        const data = await new Promise((resolve, reject) => {
            socket.emit('request_game_data');
            initializeRequestGameDataPromise().then(resolve).catch(reject);
        });
        return data;
    } catch (error) {
        console.error('Error requesting game data:', error);
        throw error;
    }
}

// todo: remove this once we have player creation set up. Or refactor it to only be ran if a guest joins
// todo: This is functionally similar to initializePlayerJoinListener
requestGameData().then(data => {
    console.log("Attempting to create player div")
    const playerDiv = createPlayerDiv('Taylor', data)
    document.getElementById('player-container').appendChild(playerDiv);
}).catch(error => {
    console.error('Failed to fetch game data:', error);
});
