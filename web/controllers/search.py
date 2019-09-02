from web import app

from flask import send_from_directory, request, redirect, render_template

import csv
import os

#@app.route('/search')
#def search():
#
#    csv_file = os.path.join(os.path.dirname(__file__), '..', 'assets', 'freshmen.csv')
#    print("Getting started")
#    freshmen = []
#
#    with open(csv_file, encoding='utf-8') as data:
#
#        reader = csv.reader(data, delimiter=',')
#
#        for freshman in reader:
#            profile = {
#                'name': freshman[0] + ' ' + freshman[1],
#                'email': freshman[2],
#                'phone': freshman[3]
#            }
#
#            freshmen.append(profile)
#
#    return render_template('search.html', freshmen=freshmen)
