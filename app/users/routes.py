from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db, bcrypt
from sqlalchemy import func
from app.users.forms import SignupForm, LoginForm, UpdateAccountForm,RequestResetForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handle user registration.

    Returns:
        str: The HTML content of the rendered 'signup.html' template.

    Example:
        The function is a Flask route handler for the '/signup' route.
        It handles the form submission for user registration and redirects to the login page upon success.
    """

    if current_user.is_authenticated:
        return redirect(url_for('tasks.dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('signup.html', title='Sign up', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    Returns:
        str: The HTML content of the rendered 'login.html' template.

    Example:
        The function is a Flask route handler for the '/login' route.
        It handles the form submission for user login and redirects to the dashboard upon success.
    """

    if current_user.is_authenticated:
        return redirect(url_for('tasks.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(func.lower(User.email) == func.lower(form.email.data)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user, remember=form.remember_me.data)
           return redirect(url_for('tasks.dashboard'))
        else:
            flash('Wrong email or password.')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    """
    Handle user logout.

    Returns:
        Response: A redirect response to the login page.

    Example:
        The function is a Flask route handler for the '/logout' route.
        It logs out the current user and redirects to the login page.
    """

    logout_user()
    return redirect(url_for('users.login'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """
    Handle user account settings.

    Returns:
        str: The HTML content of the rendered 'account.html' template.

    Example:
        The function is a Flask route handler for the '/account' route.
        It handles the form submission for updating user account information and redirects to the account page upon success.
    """

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('account.html', title='Profile', image_file=image_file, form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    """
    Handle user password reset request.

    Returns:
        str: The HTML content of the rendered 'reset_request.html' template.

    Example:
        The function is a Flask route handler for the '/reset_password' route.
        It handles the form submission for requesting a password reset and displays a success message.
    """

    if current_user.is_authenticated:
        return redirect(url_for('users.logout'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter(func.lower(User.email) == func.lower(form.email.data)).first()
        send_reset_email(user)
        flash('Email successfully sent!!')
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """
    Handle user password reset with a token.

    Args:
        token (str): The reset token.

    Returns:
        str: The HTML content of the rendered 'reset_token.html' template.

    Example:
        The function is a Flask route handler for the '/reset_password/<token>' route.
        It validates the token, handles the form submission for resetting the password, and displays a success message.
    """
    
    if current_user.is_authenticated:
         return redirect(url_for('users.logout'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or Expired token')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password update successful!!')
    return render_template('reset_token.html', title='Reset Password', form=form)