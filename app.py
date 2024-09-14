from flask import Flask, render_template, redirect, url_for
from models import db, User
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from socketio_instance import socketio  # Import from socketio_instance.py
from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp
from flask_scss import Scss
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xe0\x16t\xd2\xa5\x14\xfaR[\x19\x96\x07\x9c\x0c\x97_g\xd2\xc8\x11Q\t]\xc6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tobijahekprikpe@gmail.com'
app.config['MAIL_PASSWORD'] = 'mynameisyourname'

# Upload folder configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/profile_pics')

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Initialize Flask-Mail
mail = Mail(app)

# Serializer for generating and verifying tokens
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# User loader callback function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

socketio.init_app(app)  # Initialize socketio with the app

# Initialize Flask-Scss
Scss(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(chat_bp, url_prefix='/chat')

@app.route('/')
def index():
    username = current_user.username if current_user.is_authenticated else 'Guest'
    return render_template('index.html', username=username)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, debug=True)