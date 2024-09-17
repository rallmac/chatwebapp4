// static/chat.js
var socket = io();

function setUsername() {
    var usernameInput = document.getElementById('username');
    if (usernameInput) {
        var username = usernameInput.value;
        socket.emit('username', username);
    } else {
        console.error('Username input element not found');
    }
}

socket.on('connect', function() {
    var username = prompt("Please enter your name:");
    if (username) {
        socket.emit('username', username);
    }
});

socket.on('message', function(msg) {
    var messagesList = document.getElementById('messages');
    if (messagesList) {
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(msg));
        messagesList.appendChild(li);
    } else {
        console.error('Messages list element not found');
    }
});

function sendMessage() {
    var messageInput = document.getElementById('message');
    var roomInput = document.getElementById('room');
    
    if (messageInput && roomInput) {
        var message = messageInput.value;
        var room = roomInput.value;
        socket.emit('message', { message: message, room: room });
        messageInput.value = '';
    } else {
        console.error('Message or room input element not found');
    }
}
