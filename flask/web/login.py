from flask import flash, request, redirect, render_template, url_for
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user

from . import app
from .models import User

# begin user access management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(uid):
    return User.get(uid)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    endpoint = request.form['sign-out-endpoint']
    logout_user()
    # flash('Logged out successfully.', 'success')
    return redirect(url_for(endpoint))

# # next_is_valid should check if the user has valid
# # permission to access the `next` url
# def next_is_valid(n):
#     return current_user.is_authenticated

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect('/')

    next = request.args.get('next')  # THIS IS NEEDED ?

    if request.method == 'POST':
        endpoint = request.form['sign-in-endpoint']
        uid = str(request.form['uid']).strip().upper()
        user = User(uid)
        login_user(user)
        return redirect(url_for(endpoint))

    return redirect('/')

