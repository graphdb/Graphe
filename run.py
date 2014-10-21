#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Graphe import app

app.secret_key = 'development'

if __name__ == '__main__':
    app.run(debug=True)
