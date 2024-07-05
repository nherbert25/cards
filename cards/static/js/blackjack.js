// https://www.youtube.com/watch?v=4K33w-0-p2c   good video on xml http requests  (callbacks?)
// https://www.youtube.com/watch?v=23hrM4saaMk    rebuilding the last video with the fetch api instead (it's more modern)
// look up async/await. I *think* they're built on top of promises. They're a wrapper that makes the code more readable, yet under the hood they're still promises.
// from my 1 second google, you still write your promise, then your other function will be defined as an async function by adding it as a keyword
// in the definition, aka: "async function myFunction() { ...my code ..  await myPromise() ... my code ..  }"
// https://www.youtube.com/watch?v=AMp6hlA8xKA   using websockets instead of fetch and callbacks


const socket = io();

// Log when the client is connected
socket.on('connect', function () {
    console.log('Connected to server');
});

// Log all incoming events
socket.onAny((event, ...args) => {
    console.log(event, args);
});

socket.on('update_button_counts', function (data) {
    // Handle button count updates for the selected game
    document.getElementById('button1-count').innerText = data.counts.button1;
    document.getElementById('button2-count').innerText = data.counts.button2;
    console.log(data.counts);
});

// Function to press a button
function pressButton(buttonNumber) {
    socket.emit('press_button', {'buttonNumber': buttonNumber});
};




document.addEventListener('DOMContentLoaded', (event) => {
    socket.on('update_page_data', function (data) {
        for (const [key, value] of Object.entries(data)) {
            // replaces python syntax 'your_coins' with html syntax 'your-coins'
            key.replace(/_/g, '-')
            const element = document.getElementById(key);
            if (element) {
                element.innerText = value;
            }
        }
        console.log(data);
    });
});


// document.addEventListener('DOMContentLoaded', (event) => {
//     socket.on('update_game_state', function (data) {
//         document.getElementById('dealer-cards').innerHTML = generateCardImages(data.dealer_cards);
//         document.getElementById('player-cards').innerHTML = generateCardImages(data.player_cards);
//         document.getElementById('message').innerText = data.message;
//         document.getElementById('hit').disabled = !data.can_hit;
//         document.getElementById('stay').disabled = !data.can_stay;
//     });
// });