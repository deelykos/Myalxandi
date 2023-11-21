import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
app.config['CKEDITOR_HEIGHT'] = 100  # px
app.config['CKEDITOR_WDITH'] = 40  # px
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'fabianohaz@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
mail = Mail(app)

bcrypt = Bcrypt(app)
ckeditor = CKEditor(app)

from app import routes, models
