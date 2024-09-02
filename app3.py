#!/usr/bin/python3

from flask import Flask, render_template
from flask_socketio import SocketIO, send


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xa6\xbc\xc4P\x9a\x906\xd7z\xcbU\xac5{\x7fG \xfcZ\x9f@\x87$W'
socketio = SocketIO(app)


# Route for the chat page
@app.route('/')
def chat():
    return render_template('chat.html')


# Handle incoming message
@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
