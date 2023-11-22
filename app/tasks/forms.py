from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'class': 'my-class'})
    description = CKEditorField('Description')
    resources = CKEditorField('Study Materials')
    challenges = CKEditorField('Challenges')
    achievements = CKEditorField('Achievements')
    submit = SubmitField('Save Task', render_kw={'class': 'my-submit'})