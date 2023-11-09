from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import SignupForm, LoginForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('add_task'))
    return render_template('login.html', title='Login', form=form)

@app.route('/dashboard')
def dashboard():
    # Implement displaying user tasks on the dashboard
    pass

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    return render_template('add_task.html')

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # Implement editing an existing task logic here
    pass

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    # Implement deleting a task logic here
    pass