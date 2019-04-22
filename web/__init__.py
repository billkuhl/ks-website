from flask import Flask

app = Flask(__name__)

from flask import request
from werkzeug import url_encode

# Set up configs
import web.config as config
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up Database
from web.models import db
db.app = app
db.init_app(app)

app.config['APP_NAME'] = config.APP_NAME

# from flask_login import LoginManager

# login = LoginManager(app)

import web.controllers