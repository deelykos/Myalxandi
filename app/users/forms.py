from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from sqlalchemy import func
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User



class SignupForm(FlaskForm):
    """
    Form for user registration.

    Attributes:
        username (StringField): The username for registration.
        email (StringField): The email for registration.
        password (PasswordField): The password for registration.
        confirm_password (PasswordField): Confirmation of the password.
        submit (SubmitField): The button to submit the registration form.

    Methods:
        validate_username(self, username): Custom validation to check if the username already exists.
        validate_email(self, email): Custom validation to check if the email already exists.

    Example:
        The `SignupForm` can be used in a Flask route to handle user registration.
        It includes fields for the username, email, password, and confirmation password.
        The form can be rendered in an HTML template to allow users to sign up.
    """

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=6)], render_kw={'class': 'my-class'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'my-class'}) 
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)], render_kw={'class': 'my-class'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={'class': 'my-class'})
    submit = SubmitField('Sign Up', render_kw={'class': 'my-submit'})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exits.')

        
    def validate_email(self, email):
        if User.query.filter(func.lower(User.email) == func.lower(email.data)).first():
            raise ValidationError('Email address already exits.')



class LoginForm(FlaskForm):
    """
    Form for user login.

    Attributes:
        email (StringField): The email for login.
        password (PasswordField): The password for login.
        remember_me (BooleanField): Option to remember the user.
        submit (SubmitField): The button to submit the login form.

    Example:
        The `LoginForm` can be used in a Flask route to handle user login.
        It includes fields for the email, password, and an option to remember the user.
        The form can be rendered in an HTML template to allow users to log in.
    """

    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'my-class'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': 'my-class'})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login', render_kw={'class': 'my-submit'})


class UpdateAccountForm(FlaskForm):
    """
    Form for updating user account information.

    Attributes:
        username (StringField): The updated username.
        email (StringField): The updated email.
        picture (FileField): File field for updating the profile picture.
        submit (SubmitField): The button to submit the update form.

    Methods:
        validate_username(self, username): Custom validation to check if the username already exists.
        validate_email(self, email): Custom validation to check if the email already exists.

    Example:
        The `UpdateAccountForm` can be used in a Flask route to handle updating user account information.
        It includes fields for the updated username, email, and profile picture.
        The form can be rendered in an HTML template to allow users to update their account details.
    """

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=6)], render_kw={'class': 'my-class'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'my-class'})
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])], render_kw={'class': 'my-class'})
    submit = SubmitField('Update', render_kw={'class': 'my-submit'})

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Username already exits.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter(func.lower(User.email) == func.lower(email.data)).first()
            if user is not None:
                raise ValidationError('Email address already exits.')
            

class RequestResetForm(FlaskForm):
    """
    Form for requesting a password reset.

    Attributes:
        email (StringField): The email for requesting a password reset.
        submit (SubmitField): The button to submit the reset request.

    Methods:
        validate_email(self, email): Custom validation to check if the email exists.

    Example:
        The `RequestResetForm` can be used in a Flask route to handle password reset requests.
        It includes a field for the email, and the form can be rendered in an HTML template.
    """

    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'my-class'})
    submit = SubmitField('Request Password Reset', render_kw={'class': 'my-submit'})

    def validate_email(self, email):
         user = User.query.filter(func.lower(User.email) == func.lower(email.data)).first()
         if user is None:
            raise ValidationError('Kindly signup first.')
        

class ResetPasswordForm(FlaskForm):
    """
    Form for resetting the password.

    Attributes:
        password (PasswordField): The new password.
        confirm_password (PasswordField): Confirmation of the new password.
        submit (SubmitField): The button to submit the password reset.

    Example:
        The `ResetPasswordForm` can be used in a Flask route to handle resetting the password.
        It includes fields for the new password and confirmation.
        The form can be rendered in an HTML template to allow users to reset their password.
    """
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)], render_kw={'class': 'my-class'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={'class': 'my-class'})
    submit = SubmitField('Reset Password', render_kw={'class': 'my-submit'})