import os

from flask import render_template
from flask_mail import Message

from web import app
from web import mail


def send_email(recipient, subject, template, **kwargs):
    with app.app_context():
        msg = Message(
            subject,
            sender=("TS Cobb", "tscobb.mit@gmail.com"),
            recipients=[recipient])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)
