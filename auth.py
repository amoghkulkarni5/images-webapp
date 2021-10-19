from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db, mail
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
import string
import random


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        flash(f"You are already logged in as {current_user.name}!")
        return render_template('profile.html', role=current_user.role)

    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email_id = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # check if the user actually exists
    user = User.query.filter_by(email=email_id).first()

    if not user:
        flash('User not found.')
        return redirect(url_for('auth.login'))

    if not check_password_hash(user.password, password):
        flash('Incorrect Credentials.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        if check_password_hash(current_user.password, old_password):
            current_user.password = generate_password_hash(new_password, method='sha256')
            db.session.commit()
            flash('Password Successfully Updated')
            return render_template('profile.html')
        else:
            flash('Incorrect password provided')
            return render_template('change_password.html')

    return render_template('change_password.html')

@auth.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        new_user = User(name=name, email=email, password=generate_password_hash(password, method='sha256'), role='user')
        db.session.add(new_user)
        db.session.commit()

        flash(f"User '{new_user.name}' Added")
        return render_template('profile.html', role=current_user.role)

    return render_template('add_user.html', role=current_user.role)


@auth.route('/remove-user', methods=['GET', 'POST'])
def remove_user():
    if request.method == 'POST':
        uid = request.form.get('uid')

        obj = User.query.filter_by(id=uid).one()
        db.session.delete(obj)
        db.session.commit()

        # TODO: Remove image folder

        flash('User successfully removed.')
        return render_template('profile.html', role=current_user.role)

    users = User.query.filter_by(role='user')
    return render_template('remove_user.html', users=users)


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email_id = request.form.get('email')

        # check if the user actually exists
        user = User.query.filter_by(email=email_id).first()
        if not user:
            flash('User with given email does not exist')
            return render_template('forgot_password.html')

        new_password = id_generator()
        user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()
        msg = Message('Password Recovery - Image Webapp', sender = 'images.webapp@gmail.com', recipients = [f"<{user.email}>"])
        msg.body = f"Hi, <br> your new password is {new_password}. Kindly change your password when you login again and delete this message. <br> Thanks!"
        mail.send(msg)
        return render_template('sent_recovery_email.html')

    return render_template('forgot_password.html')

#---------------Helper Functions-----------------------

def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))