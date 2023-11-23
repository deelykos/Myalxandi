import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    Configuration class for the Flask application.

    Attributes:
        SECRET_KEY (str): The secret key used for cryptographic operations.
        SQLALCHEMY_DATABASE_URI (str): The URI for the application's database.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Whether to track modifications to database objects.
        CKEDITOR_HEIGHT (int): The height of the CKEditor in pixels.
        CKEDITOR_WIDTH (int): The width of the CKEditor in pixels.
        MAIL_SERVER (str): The SMTP server for sending emails.
        MAIL_PORT (int): The port used for email communication.
        MAIL_USE_SSL (bool): Whether to use SSL for email communication.
        MAIL_USE_TLS (bool): Whether to use TLS for email communication.
        MAIL_USERNAME (str): The email address used for sending emails.
        MAIL_PASSWORD (str): The password for the email account.

    Example:
        The Config class is used to store configuration settings for the Flask application.
        It includes settings for the secret key, database URI, CKEditor dimensions, and email configuration.
    """
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you wish'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_HEIGHT = 100  # px
    CKEDITOR_WDITH = 40  # px
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'fabianohaz@gmail.com'
    MAIL_PASSWORD = os.environ.get('PASSWORD')