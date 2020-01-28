from flask import Flask

app = Flask(__name__)

# Set up configs
import web.config as config

app.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ADMIN_EMAIL"] = config.ADMIN_EMAIL
app.config["MAIL_SERVER"] = config.MAIL_SERVER
app.config["MAIL_PORT"] = config.MAIL_PORT
app.config["MAIL_USE_SSL"] = config.MAIL_USE_SSL
app.config["MAIL_USERNAME"] = config.MAIL_USERNAME
app.config["MAIL_PASSWORD"] = config.MAIL_PASSWORD

app.secret_key = config.SECRET

# Set up login_manager
from flask_login import LoginManager

login_manager = LoginManager(app)

login_manager.session_protection = "strong"
# login_manager.login_view = 'account.login' FOLDER_UNDER_TEMPLATES.HTML_FILE.html
login_manager.init_app(app)

from flask_mail import Mail

# Set up mail
mail = Mail()
mail.init_app(app)

# Set up Database
from web.models import db

db.app = app
db.init_app(app)

app.config["APP_NAME"] = config.APP_NAME

from flask_rq import RQ

RQ(app)


@app.template_test()
def equalto(value, other):
    return value == other


@app.template_global()
def is_hidden_field(field):
    from wtforms.fields import HiddenField

    return isinstance(field, HiddenField)

    app.add_template_global(index_for_role)


import web.controllers
