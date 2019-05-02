from web.utils import *
from web.controllers.forms import UpdateUserForm, ChangePasswordForm
from web.models import User
from flask import Blueprint, url_for, render_template, abort, flash
from flask_login import login_required

settings = Blueprint('settings', __name__)

@settings.route('/', methods=['GET', 'POST'])
@settings.route('/profile', methods=['GET', 'POST'])
@login_required
def index():
    """User settings page."""
    user = current_user
    form = UpdateUserForm()
    try:
        if form.validate_on_submit():
            filtered = {k: v for k,v in form.data.items() if v != '' and str(v) != 'None' and k != 'submit' and k != 'csrf_token'}
            # user.update(kwargs=filtered)
            for key, value in filtered.items():
                setattr(user, key, value)
            print(user.class_year)
            db.session.commit()
            print(user)
            flash('User "{}" successfully updated'.format(user.full_name()),
              'form-success')
    except Exception as e:
        print(e)

    return render_template('account/settings/profile.html', user=user, form=form)

@settings.route('/admin', methods=['GET', 'POST'])
@login_required
def account():
    """User settings admin page"""
    user = current_user
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():
        # First, check old password
        if user.verify_password(change_password_form.old_password.data):
            user.password = change_password_form.new_password.data
            db.session.commit()
            flash('Your password has been updated.', 'form-success')
        else:
            flash('Original password is invalid.', 'form-error')

    return render_template('account/settings/admin.html', user=user, form=change_password_form)