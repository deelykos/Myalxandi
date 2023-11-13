from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)], render_kw={'class': 'my-class'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'my-class'}) 
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)], render_kw={'class': 'my-class'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={'class': 'my-class'})
    submit = SubmitField('Sign Up', render_kw={'class': 'my-submit'})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exits.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address already exits.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'my-class'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': 'my-class'})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login', render_kw={'class': 'my-submit'})
