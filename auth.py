from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from flask_login import login_user, logout_user, login_required
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # check if the user actually exists
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/logout')
def logout():
    return 'Logout'


@auth.route('/signup')
def signup():
    return render_template('signup.html')
