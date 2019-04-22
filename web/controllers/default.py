from web import app
from web.utils import *
from web.models import *
from web.models.user import *

import os
import json

from flask import send_from_directory, request, redirect, render_template

@app.route('/restricted')
@requires_auth()
def restricted():
    users = User.query.all()
    print(users)
    return render_template('restricted.html')

# Display the summer housing page
@app.route('/summer-housing')
def summer_housing():
    return render_template('summer-housing.html')

# Display the home page
@app.route('/about')
@app.route('/')
def index():
    return render_template('home.html')