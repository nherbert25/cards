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
// TODO: only call this function if FLASK_ENV=development
export function generateDebuggerElement() {
    try {
        const socketTestingContainer = document.getElementById('socket-button-testing-container');
        socketTestingContainer.appendChild(createSocketButtonTestingDiv());
    }
    catch (error) {
        console.error('generateDebuggerElement error:', error);
    }
}
