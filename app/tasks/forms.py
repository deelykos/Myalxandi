from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


class TaskForm(FlaskForm):
    """
    Form for creating or editing a task.

    Attributes:
        title (StringField): The title of the task.
        description (CKEditorField): The description of the task.
        resources (CKEditorField): Study materials related to the task.
        challenges (CKEditorField): Challenges associated with the task.
        achievements (CKEditorField): Achievements related to the task.
        submit (SubmitField): The button to save the task.

    Example:
        The `TaskForm` can be used in a Flask route to handle task creation or editing.
        It includes fields for the title, description, study materials, challenges, and achievements.
        The form can be rendered in an HTML template to allow users to input information about a task.
    """
    
    title = StringField('Title', validators=[DataRequired()], render_kw={'class': 'my-class'})
    description = CKEditorField('Description')
    resources = CKEditorField('Study Materials')
    challenges = CKEditorField('Challenges')
    achievements = CKEditorField('Achievements')
    submit = SubmitField('Save Task', render_kw={'class': 'my-submit'})