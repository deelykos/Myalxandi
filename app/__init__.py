from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
app.config['CKEDITOR_HEIGHT'] = 100  # px
app.config['CKEDITOR_WDITH'] = 40  # px


bcrypt = Bcrypt(app)

ckeditor = CKEditor(app)

from app import routes, models
