# -*- coding: utf-8 -*-

from . import app
from py2neo import Graph

graph = Graph(app.config['NEO4J_DATABASE_URL'])
