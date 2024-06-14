#!/usr/bin/python3
from flask import current_app as app
from flask import render_template

from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

