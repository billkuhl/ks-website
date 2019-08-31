from web import app

import os
import json
import datetime

from flask import send_from_directory, request, redirect, render_template

# Display the summer housing page
@app.route('/rush')
def rush():
    ok_date = datetime.datetime(year=2019, month=8, day=31, hour=3, minute=59, second=59)
    show = datetime.datetime.now() > ok_date
    return render_template('rush.html', show=show)

# Display the summer housing page
@app.route('/summer-housing')
def summer_housing():
    return render_template('summer-housing.html')

@app.route('/form')
def entry_form():
    return redirect('https://www.docs.google.com/forms/d/e/1FAIpQLSdagonMXv1AGXdZAoMynzV5ycG22IR_l-HrXYCKiqudZnJA9Q/viewform?usp=sf_link')

# Display the home page
@app.route('/about')
@app.route('/')
def index():
    return render_template('home.html')