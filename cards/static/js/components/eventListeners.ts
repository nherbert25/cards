import {BlackjackData, Card, Hand, Player} from "./schemas.js";
import {createHandDiv, createPlayerDiv, updatePageData} from "./gameUI.js";

// TODO: get the import { io } to work and remove from html
//  import { io } from "https://cdn.socket.io/4.7.4/socket.io.esm.min.js";
//  import { io } from 'socket.io-client';
declare const io: any;
const socket = io();


export function setUpEventListeners() {
    initializeOnConnectionListener();
    initializeUpdatePageListener();
    initializePlayerAddedHandListener();
    initializeRebuildEntirePage()
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



// function initializePlayerJoinListener() {
//     socket.on('player_joined', function (data: Player) {
//         const playerDiv = createPlayerDiv(data.playerID, data.playerData);
//         document.getElementById('player-container')!.appendChild(playerDiv);
//     });
// }


function initializeRebuildEntirePage() {
    socket.on('rebuild_entire_page', function (data: BlackjackData) {
        try {
            console.log("initializeRebuildEntirePage triggered with: ", data);

            // reset and repopulate player-container
            const playerContainer = document.getElementById('player-container')!;
            playerContainer.innerHTML = '';

            const playersData = data.players;
            for (const [playerID, playerData] of Object.entries(playersData)) {
                const playerDiv = createPlayerDiv(playerID, playerData);
                playerContainer.appendChild(playerDiv);
            }

            updatePageData(data);

        } catch (error) {
            console.error('Failed to fetch game data:', error);
        }
    });
}







