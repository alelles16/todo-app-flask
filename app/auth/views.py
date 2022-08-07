from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash
from . import auth
from .forms import LoginForm, TodoForm
from app.firestore_service import (
    get_todos, get_user, user_put, put_todo, delete_todo_of_todos)
from .models import UserData, UserModel


@auth.route('/login', methods=['get', 'post'])
def login():
    """
    Login for users
    """
    # Instance of LoginForm
    login_form = LoginForm()

    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)
        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']
            if password_from_db == password:
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                session['username'] = username

                return redirect(url_for('auth.me'))
            else:
                flash('Username or password are incorrect')
        else:
            flash('User not found')

    return render_template('login.html', **context)


@auth.route('/me', methods=['get', 'post'])
@login_required
def me():
    """
    My profile for users
    """
    username = current_user.id
    # username = session.get('username')

    todos = get_todos(username)
    todo_form = TodoForm()

    context = {
        'username': username,
        'todos': todos,
        'todo_form': todo_form
    }

    if todo_form.validate_on_submit():
        put_todo(username, todo_form.description.data)
        flash('Task added')
        return redirect(url_for('auth.me'))

    return render_template('me.html', **context)


@auth.route('/todos/delete/<todo_id>', methods=['get', 'post'])
@login_required
def delete_todo(todo_id):
    user_id = current_user.id
    delete_todo_of_todos(user_id, todo_id)
    return redirect(url_for('auth.me'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bye bye!')
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['get', 'post'])
def sign_up():
    signup_form = LoginForm()
    context = {
        "signup_form": signup_form
    }
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)
        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data)
            user = UserModel(user_data)

            login_user(user)

            return redirect(url_for('auth.me'))
        else:
            flash(f'User with name: {username} already exist!')

    return render_template('signup.html', **context)
