import { createHandDiv, createPlayerDiv, updatePageData } from "./gameUI.js";
const socket = io();
export function setUpEventListeners() {
    // await initializePlayerDivs();
    // Set up the socket connection to the Python backend (probably via WebSocket or HTTP)
    initializeOnConnectionListener();
    initializeUpdatePageListener();
    // initializePlayerJoinListener();
    initializePlayerAddedHandListener();
    initializeButtonCountsListener();
    initializeNewGameListener();
    console.log("DOM fully loaded.");
}
function initializeOnConnectionListener() {
    socket.on('connect', function () {
        console.log('Connected to server');
    });
}
function initializeUpdatePageListener() {
    socket.on('update_page_data', updatePageData);
}
;
function initializePlayerAddedHandListener() {
    socket.on('player_added_hand', function (data) {
        console.log("Running player_added_hand with: ", data);
        const { player_id, player_data } = data;
        const handIndex = player_data.hands.length - 1;
        const newHandDiv = createHandDiv(player_id, handIndex.toString(), player_data, player_data.hands[handIndex]);
        const existingPlayerDiv = document.getElementById('player-' + player_id);
        existingPlayerDiv.appendChild(newHandDiv);
    });
}
function initializeButtonCountsListener() {
    socket.on('update_button_counts', function (data) {
        // Handle button count updates for the selected game
        document.getElementById('button1-count').innerText = data.counts.button1.toString();
        document.getElementById('button2-count').innerText = data.counts.button2.toString();
    });
}
// function initializePlayerJoinListener() {
//     socket.on('player_joined', function (data: Player) {
//         const playerDiv = createPlayerDiv(data.playerID, data.playerData);
//         document.getElementById('player-container')!.appendChild(playerDiv);
//     });
// }
function initializeNewGameListener() {
    socket.on('initialize_new_game', function (data) {
        try {
            console.log("initializeNewGameListener triggered with: ", data);
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
        }
        catch (error) {
            console.error('Failed to fetch game data:', error);
        }
    });
}
