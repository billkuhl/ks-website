from flask import Blueprint, flash, render_template, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user
from flask_rq import get_queue
from web.mail import send_email
from web.controllers.forms import *
from web.utils import *

account = Blueprint('account', __name__)


@account.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if current_user.is_authenticated:
        flash('Already logged in. Want to log out?', 'info')
        return redirect(url_for('main.brother_portal'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_hash is not None and \
                user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('You are now logged in. Welcome back!', 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid email or password.', 'form-error')
    return render_template('account/login.html', form=form)


@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@account.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    """Respond to existing user's request to reset their password."""
    print(current_user)
    print(current_user.is_anonymous)
    if not current_user.is_anonymous:
        print('hey')
        return redirect(url_for('main.index'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        print(form.email.data)
        if user:
            token = user.generate_password_reset_token()
            print(token)
            token = token.decode('utf-8')
            reset_link = url_for(
                'account.reset_password', token=token, _external=True)
            print(reset_link)
            send_email(
                recipient=user.email,
                subject='Reset Your Password',
                template='account/email/reset_password',
                user=user,
                reset_link=reset_link,
                next=request.args.get('next'))

            # get_queue().enqueue(
            #     send_email,
            #     recipient=user.email,
            #     subject='Reset Your Password',
            #     template='account/email/reset_password',
            #     user=user,
            #     reset_link=reset_link,
            #     next=request.args.get('next'))
        flash('A password reset link has been sent to {}.'.format(
            form.email.data), 'warning')
        return redirect(url_for('account.login'))
    return render_template('account/reset_password.html', form=form)

@account.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset an existing user's password."""
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    print('heh')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Invalid email address.', 'form-error')
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.new_password.data):
            flash('Your password has been updated.', 'form-success')
            return redirect(url_for('account.login'))
        else:
            flash('The password reset link is invalid or has expired.',
                  'form-error')
            return redirect(url_for('main.index'))
    return render_template('account/reset_password.html', form=form)