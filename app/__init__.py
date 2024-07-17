#!/usr/bin/python3
from flask import Flask
"""This module initializes a Flask application instance. """


def create_app():
    """
    Creates and configures the Flask application.

    Returns:
        app (Flask): The Flask application instance.
    """
    app = Flask(__name__)

    with app.app_context():
        
        from . import routes
    return app
