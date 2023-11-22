from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from sqlalchemy import func
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User



class SignupForm(FlaskForm):
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
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'my-class'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': 'my-class'})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login', render_kw={'class': 'my-submit'})


class UpdateAccountForm(FlaskForm):
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
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'my-class'})
    submit = SubmitField('Request Password Reset', render_kw={'class': 'my-submit'})

    def validate_email(self, email):
         user = User.query.filter(func.lower(User.email) == func.lower(email.data)).first()
         if user is None:
            raise ValidationError('Kindly signup first.')
        

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)], render_kw={'class': 'my-class'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={'class': 'my-class'})
    submit = SubmitField('Reset Password', render_kw={'class': 'my-submit'})