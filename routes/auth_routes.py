from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail

auth_bp = Blueprint('auth', __name__)

# Serializer for generating and verifying tokens
s = URLSafeTimedSerializer(b'\xe0\x16t\xd2\xa5\x14\xfaR[\x19\x96\x07\x9c\x0c\x97_g\xd2\xc8\x11Q\t]\xc6')

# Initialize Flask-Mail
mail = Mail()

# Home page
@auth_bp.route('/')
def home():
    return render_template('index.html')

# Chat page
@auth_bp.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.chat'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('auth.chat'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html')

@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt='password-reset-salt')
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            msg = Message('Password Reset Request', sender='noreply@yourapp.com', recipients=[email])
            msg.body = f'Please click the link to reset your password: {reset_url}'
            mail.send(msg)
            flash('A password reset link has been sent to your email.', 'info')
        else:
            flash('Email address not found.', 'error')
    return render_template('reset_password_request.html')

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)  # Token valid for 1 hour
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('auth.reset_password_request'))

    if request.method == 'POST':
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('User not found.', 'error')
            return redirect(url_for('auth.reset_password_request'))
    return render_template('reset_password.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('auth.chat'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form['username']
        # Add other profile fields as needed
        current_user.username = username
        # Update other fields as needed
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('auth.chat'))
    return render_template('edit_profile.html', user=current_user)

@auth_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = current_user.id
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Your account has been deleted.', 'success')
        logout_user()
        return redirect(url_for('auth.home'))
    else:
        flash('Account deletion failed. User not found.', 'danger')
        return redirect(url_for('auth.edit_profile'))

@auth_bp.route('/view_users')
@login_required
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)

@auth_bp.route('/search')
@login_required
def search():
    query = request.args.get('query')
    # Handle search logic here
    return render_template('search_results.html', query=query)