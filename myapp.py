from app import create_app

app = create_app()

if __name__ == '__main__':
    """
    Run the Flask application.

    Example:
        The script creates a Flask application using the create_app function.
    """
    app.run(debug=True, host='0.0.0.0')