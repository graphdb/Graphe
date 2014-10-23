# -*- coding: utf-8 -*-

import os

FACEBOOK_APP_ID = '539322962865082'
FACEBOOK_APP_SECRET = 'bb32c614be336ba032605ef00873f1ed'
NEO4J_DATABASE_URL = '%sdb/data/' % \
                     os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474/')
