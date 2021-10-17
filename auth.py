from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from .models import User


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email_id = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # check if the user actually exists
    user = User.query.filter_by(email=email_id).first()
    print("--- USER ---")
    print(not user)

    if not user:
        flash('User not found.')
        return redirect(url_for('auth.login'))

    if user.password != password:
        flash('Incorrect Credentials.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        new_user = User(name=name, email=email, password=password, role='user')
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
