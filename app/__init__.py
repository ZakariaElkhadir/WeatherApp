#!/usr/bin/python3
from flask import Flask


def create_app():
    """
    Creates and configures the Flask application.

    Returns:
        app (Flask): The Flask application instance.
    """
    app = Flask(__name__)

    with app.app_context():
        # Import routes
        from . import routes
    return app
