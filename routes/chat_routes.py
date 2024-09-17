from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from flask_socketio import send, join_room, leave_room
from models import db, User
from socketio_instance import socketio  # Import from socketio_instance.py

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@chat_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search_user():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            room = f'chat_{min(current_user.username, username)}_{max(current_user.username, username)}'
            return redirect(url_for('chat.private_chat', room=room))
    return render_template('search.html')

@chat_bp.route('/chat/<room>')
@login_required
def private_chat(room):
    return render_template('private_chat.html', room=room, username=current_user.username)

@socketio.on('message')
def handle_message(data):
    if current_user.is_authenticated:
        msg = data['message']
        room = data['room']
        send(f'{current_user.username}: {msg}', room=room)
    else:
        send('User not authenticated')

@socketio.on('join')
def on_join(data):
    if current_user.is_authenticated:
        room = data['room']
        join_room(room)
        send(f'{current_user.username} has entered the room.', room=room)
    else:
        send('User not authenticated')

@socketio.on('leave')
def on_leave(data):
    if current_user.is_authenticated:
        room = data['room']
        leave_room(room)
        send(f'{current_user.username} has left the room.', room=room)
    else:
        send('User not authenticated')
