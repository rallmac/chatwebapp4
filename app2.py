from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x89R\xaf\x00\xc7\\\xf5}\x15\x97\xaa\xfb\x0bF:I\xea2\xa5bTN|\xb7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize SocketIO
socketio = SocketIO(app)

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('chat'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def chat():
    return render_template('chat.html', username=current_user.username)

@socketio.on('message')
@login_required
def handle_message(msg):
    print('Message: ' + msg)
    send(f'{current_user.username}: {msg}', broadcast=True)

@socketio.on('username')
@login_required
def handle_username(username):
    pass  # This can be left out since we're using authenticated users

@socketio.on('disconnect')
@login_required
def handle_disconnect():
    send(f'{current_user.username} has left the chat.', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
