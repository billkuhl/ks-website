from flask import Flask

app = Flask(__name__)

from flask import request
from werkzeug import url_encode

import web.config as config

app.config['APP_NAME'] = config.APP_NAME

import web.controllers