# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)
app.config.from_object('config.common')

from . import views
from .auth import auth
app.register_blueprint(auth)
