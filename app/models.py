from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)

    def __repr__(self):
        return f"User(username='{self.username}', email='{self.email}' )"
    

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    resources = db.Column(db.Text, nullable=True)
    challenges = db.Column(db.Text, nullable=True)
    achievements = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return (
            f"Task({self.id}, title='{self.title}', "
            f"description='{self.description}', resources='{self.resources}', "
            f"challenges='{self.challenges}', achievements='{self.achievements}', "
            f"created_date={self.created_date}, due_date={self.due_date}, completed={self.completed})"
        )
