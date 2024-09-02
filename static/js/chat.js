// static/chat.js
var socket = io();

function setUsername() {
    var username = document.getElementById('username').value;
    socket.emit('username', username);
}

socket.on('connect', function() {
    var username = prompt("Please enter your name:");
    socket.emit('username', username);
});

socket.on('message', function(msg) {
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(msg));
    document.getElementById('messages').appendChild(li);
});

function sendMessage() {
    var message = document.getElementById('message').value;
    socket.send(message);
    document.getElementById('message').value = '';
}
