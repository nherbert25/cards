import {BlackjackData, Card, Hand, Player} from "./schemas.js";
import {createHandDiv, createPlayerDiv, initializePlayerDivs, updatePageData} from "./gameUI.js";

// TODO: get the import { io } to work and remove from html
//  import { io } from "https://cdn.socket.io/4.7.4/socket.io.esm.min.js";
//  import { io } from 'socket.io-client';
declare const io: any;
const socket = io();


export function setUpEventListeners() {
    initializeOnConnectionListener();
    initializeUpdatePageListener();
    initializePlayerAddedHandListener();
    initializeButtonCountsListener();
    initializeNewGameListener()
    // initializePlayerJoinListener(); // Not implemented
    console.log("DOM fully loaded.");
}


function initializeOnConnectionListener() {
    socket.on('connect', function () {
        console.log('Connected to server');
    })
}

function initializeUpdatePageListener() {
    socket.on('update_page_data', updatePageData)
};


function initializePlayerAddedHandListener() {
    socket.on('player_added_hand', function (data: { player_id: string; player_data: Player }) {
        console.log("Running player_added_hand with: ", data);
        const {player_id, player_data} = data;

        const handIndex = player_data.hands.length - 1;
        const newHandDiv = createHandDiv(player_id, handIndex.toString(), player_data, player_data.hands[handIndex]);

        const existingPlayerDiv = document.getElementById('player-' + player_id)!;
        existingPlayerDiv.appendChild(newHandDiv);
    });
}


function initializeButtonCountsListener() {
    socket.on('update_button_counts', function (data: { counts: { button1: number; button2: number } }) {
        // Handle button count updates for the selected game
        document.getElementById('button1-count')!.innerText = data.counts.button1.toString();
        document.getElementById('button2-count')!.innerText = data.counts.button2.toString();
    });
}

// function initializePlayerJoinListener() {
//     socket.on('player_joined', function (data: Player) {
//         const playerDiv = createPlayerDiv(data.playerID, data.playerData);
//         document.getElementById('player-container')!.appendChild(playerDiv);
//     });
// }


function initializeNewGameListener() {
    socket.on('initialize_new_game', function (data: BlackjackData) {
        try {
            console.log("initializeNewGameListener triggered with: ", data);

            // reset and repopulate player-container
            const playerContainer = document.getElementById('player-container')!;
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







