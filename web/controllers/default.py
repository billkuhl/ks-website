from web.models.user import *
from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


# Display the brother's only page
@main.route('/brothers')
@login_required
def brother_portal():
    return render_template('portal.html', user=current_user)


# Display the summer housing page
@main.route('/summer-housing')
def summer_housing():
    return render_template('summer-housing.html')


# Display the home page
@main.route('/about')
@main.route('/')
def index():
    return render_template('home.html')

@login_manager.unauthorized_handler
def unauthorized_callback():
    print(request.path)
    return redirect('/account/login?next=' + request.path)

