from flask import render_template, url_for, flash, redirect
from app import app, db, bcrypt
from app.forms import SignupForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Task

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('add_task'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('add_task'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user, remember=form.remember_me.data)
           return redirect(url_for('add_task'))
        else:
            flash('Wrong email or password.')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html', title='account')

@app.route('/dashboard')
@login_required
def dashboard():
    # Implement displaying user tasks on the dashboard
    pass

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    return render_template('add_task.html', title='add_task')

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    # Implement editing an existing task logic here
    pass

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    # Implement deleting a task logic here
    pass
