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
    app = Flask(__name__)
    app.config.from_object(Config)

    
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    bcrypt.init_app(app)
    ckeditor.init_app(app)


    from app.users.routes import users
    from app.tasks.routes import tasks
    from app.main.routes import main
    from app.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(tasks)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app