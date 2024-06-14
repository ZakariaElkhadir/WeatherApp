#!/usr/bin/python3
from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        # Import routes
        from . import routes
        from . import backend

    return app
