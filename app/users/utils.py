import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail

def save_picture(form_picture):
    """
    Save and resize a profile picture.

    Args:
        form_picture (FileStorage): The profile picture uploaded via a form.

    Returns:
        str: The filename of the saved picture.

    Example:
        The function can be used to save and resize a user's profile picture.
        It generates a random filename, resizes the image, and saves it to the 'static/profile_pic' directory.
    """

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pic', picture_fn)

    output_size = (100, 100)
    new_image = Image.open(form_picture)
    new_image.thumbnail(output_size)
    new_image.save(picture_path)

    return picture_fn

def send_reset_email(user):
    """
    Send a password reset email to the user.

    Args:
        user (User): The user for whom the password reset email is being sent.

    Example:
        The function can be used to send a password reset email to a user.
        It generates a reset token, constructs an email message, and sends it to the user's email address.
    """
    
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request, simply ignore this email and no changes will be made to your password.
    '''
    mail.send(msg)