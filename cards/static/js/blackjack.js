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

socket.on('update_button_counts', function (data) {
    // Handle button count updates for the selected game
    document.getElementById('button1-count').innerText = data.counts.button1;
    document.getElementById('button2-count').innerText = data.counts.button2;
    console.log(data.counts);
});

function pressButton(buttonNumber) {
    socket.emit('press_button', {'buttonNumber': buttonNumber});
};

function refresh_data() {
    socket.emit('update_page_data');
    console.log('Asking server to refresh');
};


document.addEventListener('DOMContentLoaded', (event) => {
    socket.on('update_page_data', function (data) {
        for (const [key, value] of Object.entries(data)) {

            // replaces python syntax with html syntax. Ex: 'your_coins' to 'your-coins'
            const htmlKey = key.replace(/_/g, '-')
            const element = document.getElementById(htmlKey);
            if (element) {
                element.innerText = value;
            }
        }
        console.log(data);
    });
});
