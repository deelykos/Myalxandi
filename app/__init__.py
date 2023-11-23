from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'users.login'
mail = Mail()

bcrypt = Bcrypt()
ckeditor = CKEditor()

def create_app(config_class=Config):
    """
    Create and configure the Flask application.

    Args:
        config_class (type): The configuration class to use for the application. Defaults to `Config`.

    Returns:
        Flask: The configured Flask application.

    Example:
        The function can be used to create a Flask application with the specified configuration.
        It initializes various extensions, registers blueprints, and returns the configured application.
    """

    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)

    # Initialize SQLAlchemy, Flask-Migrate, Flask-Login, Flask-Mail, Flask-Bcrypt, and Flask-CKEditor
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    ckeditor.init_app(app)

    # Register blueprints for different parts of the application
    from app.users.routes import users
    from app.tasks.routes import tasks
    from app.main.routes import main
    from app.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(tasks)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app