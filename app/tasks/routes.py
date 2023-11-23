from flask import render_template, url_for, redirect, request, jsonify, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import User, Task
from app.tasks.forms import TaskForm

tasks = Blueprint('tasks', __name__)


@tasks.route('/dashboard')
@login_required
def dashboard():
    """
    Render the user's dashboard with their tasks.

    Returns:
        str: The HTML content of the rendered 'dashboard.html' template.

    Example:
        The function is a Flask route handler for the '/dashboard' route.
        It retrieves tasks associated with the current user and renders the 'dashboard.html' template.
    """

    user = User.query.filter_by(username=current_user.username).first().tasks
    return render_template('dashboard.html', title='Dashboard', user=user)

@tasks.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    """
    Handle adding a new task.

    Returns:
        str: The HTML content of the rendered 'add_task.html' template.

    Example:
        The function is a Flask route handler for the '/add_task' route.
        It handles the form submission for adding a new task and redirects to the dashboard upon success.
    """

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
        return redirect(url_for('tasks.dashboard'))
    return render_template('add_task.html', title='New_task', form=form, legend='New Task')

@tasks.route('/task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task(task_id):
    """
    Render a specific task.

    Args:
        task_id (int): The ID of the task to be displayed.

    Returns:
        str: The HTML content of the rendered 'task.html' template.

    Example:
        The function is a Flask route handler for the '/task/<int:task_id>' route.
        It retrieves and renders a specific task based on the provided task_id.
    """

    task = Task.query.get_or_404(task_id)
    return render_template('task.html', title='Task',task=task)

@tasks.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """
    Handle editing an existing task.

    Args:
        task_id (int): The ID of the task to be edited.

    Returns:
        str: The HTML content of the rendered 'add_task.html' template.

    Example:
        The function is a Flask route handler for the '/edit_task/<int:task_id>' route.
        It handles the form submission for editing an existing task and redirects to the dashboard upon success.
    """

    task = Task.query.get_or_404(task_id)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.resources = form.resources.data
        task.challenges = form.challenges.data
        task.achievements = form.achievements.data
        db.session.commit()
        return redirect(url_for('tasks.dashboard', task_id=task.id))
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.resources.data = task.resources
        form.challenges.data = task.challenges
        form.achievements.data = task.achievements
    return render_template('add_task.html', title='Edit_task', form=form, legend='Edit Task')


@tasks.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
     """
    Handle deleting an existing task.

    Args:
        task_id (int): The ID of the task to be deleted.

    Returns:
        Response: A redirect response to the dashboard.

    Example:
        The function is a Flask route handler for the '/delete_task/<int:task_id>' route.
        It deletes the specified task and redirects to the dashboard.
    """
     
     task = Task.query.get_or_404(task_id)
     db.session.delete(task)
     db.session.commit()
     return redirect(url_for('tasks.dashboard'))


@tasks.route('/update_status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    """
    Handle updating the completion status of a task.

    Args:
        task_id (int): The ID of the task whose completion status is to be updated.

    Returns:
        JSON: A JSON response indicating the updated completion status.

    Example:
        The function is a Flask route handler for the '/update_status/<int:task_id>' route.
        It toggles the completion status of the specified task and returns a JSON response.
    """
    
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()

    return jsonify({'completed': task.completed})
