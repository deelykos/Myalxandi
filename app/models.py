from datetime import datetime, timedelta
import jwt
from flask import current_app
from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(user_id):
    """
    Load a user by user ID for Flask-Login.

    Args:
        user_id (int): The ID of the user.

    Returns:
        User: The User object corresponding to the provided user ID.

    Example:
        The function is used by Flask-Login to load a user by user ID.
        It retrieves the user from the database based on the provided user_id.
    """

    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    User model representing a registered user.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The hashed password of the user.
        image_file (str): The filename of the user's profile picture.
        tasks (relationship): A relationship to the Task model.

    Methods:
        get_reset_token(self, expires_sec=300): Generate a JWT token for password reset.
        verify_reset_token(token): Verify and decode a JWT token for password reset.

    Example:
        The User model represents a user in the application with attributes like username, email, and password.
        It includes methods for generating and verifying password reset tokens.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    tasks = db.relationship('Task', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=300):
        secret_key = current_app.config['SECRET_KEY']
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_sec)
        }
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token
    
    @staticmethod
    def verify_reset_token(token):
        secret_key = current_app.config['SECRET_KEY']
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User(username='{self.username}', email='{self.email}', password='{self.password}' )"
    
class Task(db.Model):
    """
    Task model representing a user's task.

    Attributes:
        id (int): The unique identifier for the task.
        title (str): The title of the task.
        description (str): The description of the task.
        resources (str): Study materials related to the task.
        challenges (str): Challenges associated with the task.
        achievements (str): Achievements related to the task.
        created_date (datetime): The date and time when the task was created.
        completed (bool): Indicates whether the task is completed.
        user_id (int): The user ID associated with the task.

    Example:
        The Task model represents a task in the application with attributes like title, description, and completion status.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    resources = db.Column(db.Text, nullable=True)
    challenges = db.Column(db.Text, nullable=True)
    achievements = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return (
            f"Task({self.id}, title='{self.title}', "
            f"description='{self.description}', resources='{self.resources}', "
            f"challenges='{self.challenges}', achievements='{self.achievements}', "
            f"created_date={self.created_date})"
        )
