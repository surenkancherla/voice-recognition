"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from app import app

@app.route('/home')
def home():
    """Renders the home page."""
    return "hello"