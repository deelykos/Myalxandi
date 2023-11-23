from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    """
    Handle 404 Not Found errors.

    Args:
        error (Exception): The exception object representing the 404 error.

    Returns:
        tuple: A tuple containing the rendered template for the 404 error and the HTTP status code 404.

    Example:
        The function is automatically called when a 404 error occurs during a request.
        It renders the 'errors/404.html' template and returns a tuple with the template and the status code:
        
    """

    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def error_500(error):
    """
    Handle 500 Internal Server Error.

    Args:
        error (Exception): The exception object representing the 500 error.

    Returns:
        tuple: A tuple containing the rendered template for the 500 error and the HTTP status code 500.

    Example:
        The function is automatically called when a 500 error occurs during a request.
        It renders the 'errors/500.html' template and returns a tuple with the template and the status code:
        
    """

    return render_template('errors/500.html'), 500