from flask import render_template, Blueprint

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    """
    Render the home page.

    Returns:
        str: The HTML content of the rendered 'home.html' template.

    Example:
        The function is a Flask route handler for the '/' and '/home' routes.
        It renders the 'home.html' template and returns the HTML content as a string:

    """

    return render_template('home.html')

@main.route('/about')
def contact():
    """
    Render the about page.

    Returns:
        str: The HTML content of the rendered 'about.html' template.

    Example:
        The function is a Flask route handler for the '/about' routes.
        It renders the 'about.html' template and returns the HTML content as a string:

    """

    return render_template('contact.html')
