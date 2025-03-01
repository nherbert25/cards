const socket = io();
export function createSocketButtonTestingDiv() {
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
export function generateDebuggerElement() {
    try {
        const socketTestingContainer = document.getElementById('socket-button-testing-container');
        socketTestingContainer.appendChild(createSocketButtonTestingDiv());
    }
    catch (error) {
        console.error('generateDebuggerElement error:', error);
    }
}
function initializeButtonCountsListener() {
    socket.on('update_button_counts', function (data) {
        // Handle button count updates for the selected game
        document.getElementById('button1-count').innerText = data.counts.button1.toString();
        document.getElementById('button2-count').innerText = data.counts.button2.toString();
    });
}
// // Update button counts
// if (htmlKey === "button-counts") {
//     const {button1, button2} = value;
//     document.getElementById('button1-count')!.innerText = button1;
//     document.getElementById('button2-count')!.innerText = button2;
// }
// Ensure the DOM has fully loaded before running the function
document.addEventListener('DOMContentLoaded', () => {
    generateDebuggerElement(); // This will run after the DOM is fully loaded.
    initializeButtonCountsListener();
    // press_socket_testing_buttons
});
