import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import SignupForm, LoginForm, UpdateAccountForm, TaskForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Task

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
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
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user, remember=form.remember_me.data)
           return redirect(url_for('dashboard'))
        else:
            flash('Wrong email or password.')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)

    output_size = (100, 100)
    new_image = Image.open(form_picture)
    new_image.thumbnail(output_size)
    new_image.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('account.html', title='Profile', image_file=image_file, form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.filter_by(username=current_user.username).first().tasks
    return render_template('dashboard.html', title='Dashboard', user=user)

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            resources=form.resources.data,
            challenges=form.challenges.data,
            achievements=form.achievements.data,
            user=current_user
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_task.html', title='New_task', form=form, legend='New Task')

@app.route('/task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task.html', title='Task',task=task)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.resources = form.resources.data
        task.challenges = form.challenges.data
        task.achievements = form.achievements.data
        db.session.commit()
        return redirect(url_for('dashboard', task_id=task.id))
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.resources.data = task.resources
        form.challenges.data = task.challenges
        form.achievements.data = task.achievements
    return render_template('add_task.html', title='Edit_task', form=form, legend='Edit Task')


@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
     task = Task.query.get_or_404(task_id)
     db.session.delete(task)
     db.session.commit()
     return redirect(url_for('dashboard'))