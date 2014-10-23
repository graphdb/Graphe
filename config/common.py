# -*- coding: utf-8 -*-

import os

from py2neo import ServiceRoot
from py2neo.packages.httpstream.packages.urimagic import URI

FACEBOOK_APP_ID = '539322962865082'
FACEBOOK_APP_SECRET = 'bb32c614be336ba032605ef00873f1ed'
NEO4J_DATABASE_URL = '%sdb/data/' % \
                     URI(os.getenv('GRAPHENEDB_URL', ServiceRoot.DEFAULT_URI))\
                         .resolve('/')
