from web import app

import os
import json

from flask import send_from_directory, request, redirect, render_template

# Display the summer housing page
@app.route('/rush')
def rush():
    return render_template('rush.html')

# Display the summer housing page
@app.route('/summer-housing')
def summer_housing():
    return render_template('summer-housing.html')

# Display the home page
@app.route('/about')
@app.route('/')
def index():
    return render_template('home.html')