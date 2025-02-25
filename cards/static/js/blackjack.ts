// https://www.youtube.com/watch?v=4K33w-0-p2c   good video on xml http requests  (callbacks?)
// https://www.youtube.com/watch?v=23hrM4saaMk    rebuilding the last video with the fetch api instead (it's more modern)
// look up async/await. I *think* they're built on top of promises. They're a wrapper that makes the code more readable, yet under the hood they're still promises.
// from my 1 second google, you still write your promise, then your other function will be defined as an async function by adding it as a keyword
// in the definition, aka: "async function myFunction() { ...my code ..  await myPromise() ... my code ..  }"
// https://www.youtube.com/watch?v=AMp6hlA8xKA   using websockets instead of fetch and callbacks



// import { globalFunctions } from './components/globalFunctions';
// import { initializeGame, updateUI } from './components/gameUI';
// import { socketSetup } from './components/socket';


import { Hand, Player, BlackjackData, Card, Dealer, HandOutcome } from "./components/schemas";
import { setUpEventListeners } from './components/events.js';
import { initializePlayerDivs } from './components/gameUI.js';
import { generateDebuggerElement } from "./components/debugger.js";
// import { setUpEventListeners, initializePlayerDivs } from './components/events';


// TODO: get the import { io } to work and remove from html
//  import { io } from "https://cdn.socket.io/4.7.4/socket.io.esm.min.js";
//  import { io } from 'socket.io-client';
declare const io: any;
const socket = io();


// // TODO: extending the global window is bad practice. Make the buttons modules and import them
// // Extend the global window interface
declare global {
    interface Window {
        pressHit: (user_id: string, hand_index: number) => void;
        pressStay: (user_id: string, hand_index: number) => void;
        pressDoubleDown: (user_id: string, hand_index: number) => void;
        pressSplitPair: (user_id: string, hand_index: number) => void;
        pressNewGame: () => void;
        refresh_data: () => void;
        pressSocketTestingButtons: (buttonNumber: number) => void;
    }
}


// Main function to initialize everything
function main() {
    // // Initialize game UI
    // initializeGame();

    // Set up event listeners
    setUpEventListeners();

    // // Setup WebSocket connection with the backend
    // socketSetup();

    // window.pressSocketTestingButtons = pressSocketTestingButtons;
    // window.pressHit = globalFunctions.pressHit;
    // window.pressStay = globalFunctions.pressStay;
    // window.pressDoubleDown = pressDoubleDown;
    // window.pressSplitPair = pressSplitPair;
    // window.pressNewGame = pressNewGame;
    // window.refresh_data = refresh_data;
}

main();


generateDebuggerElement();




// after the DOM has loaded, register the following event listeners
document.addEventListener('DOMContentLoaded', async (event) => {
    await initializePlayerDivs();
    generateDebuggerElement();
    refresh_data();
    // initializeOnConnectionListener();
    // initializeUpdatePageListener();
    // initializePlayerJoinListener();
    // initializePlayerAddedHandListener();
    // initializeButtonCountsListener();
    // initializeNewGameListener()
    // console.log("DOM fully loaded.");
});




function pressSocketTestingButtons(buttonNumber: number) {
    socket.emit('press_socket_testing_buttons', {'buttonNumber': buttonNumber});
};
window.pressSocketTestingButtons = pressSocketTestingButtons;

function pressHit(user_id: string, hand_index: number = 0) {
    socket.emit('hit', user_id, hand_index);
};
window.pressHit = pressHit;

function pressStay(user_id: string, hand_index: number = 0) {
    socket.emit('stay', user_id, hand_index);
};
window.pressStay = pressStay;

function pressDoubleDown(user_id: string, hand_index: number = 0) {
    socket.emit('double_down', user_id, hand_index);
};
window.pressDoubleDown = pressDoubleDown;

function pressSplitPair(user_id: string, hand_index: number = 0) {
    socket.emit('split_pair', user_id, hand_index);
};
window.pressSplitPair = pressSplitPair;

function pressNewGame() {
    socket.emit('new_game');
};
window.pressNewGame = pressNewGame;

function refresh_data() {
    socket.emit('update_page_data');
    console.log('Asking server to refresh');
};
window.refresh_data = refresh_data;








