const socket = io();
// Define button event functions
function pressSocketTestingButtons(buttonNumber) {
    socket.emit('press_socket_testing_buttons', { 'buttonNumber': buttonNumber });
}
function pressHit(user_id, hand_index = 0) {
    socket.emit('hit', user_id, hand_index);
}
function pressStay(user_id, hand_index = 0) {
    socket.emit('stay', user_id, hand_index);
}
function pressDoubleDown(user_id, hand_index = 0) {
    socket.emit('double_down', user_id, hand_index);
}
function pressSplitPair(user_id, hand_index = 0) {
    socket.emit('split_pair', user_id, hand_index);
}
function pressNewGame() {
    socket.emit('new_game');
}
function refresh_data() {
    socket.emit('update_page_data');
    console.log('Asking server to refresh');
}
window.pressHit = pressHit;
window.pressStay = pressStay;
window.pressDoubleDown = pressDoubleDown;
window.pressSplitPair = pressSplitPair;
window.pressNewGame = pressNewGame;
window.refresh_data = refresh_data;
window.pressSocketTestingButtons = pressSocketTestingButtons;
export { pressHit, pressStay, pressDoubleDown, pressSplitPair, pressNewGame, refresh_data, pressSocketTestingButtons };
