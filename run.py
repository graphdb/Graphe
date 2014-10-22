#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from Graphe import app
from Graphe.models import graph

@click.group()
def run():
    pass

@run.command()
def server():
    '''Run development server'''
    app.secret_key = 'development'
    app.run(debug=True)

@run.command()
def initdb():
    '''Initialize database'''
    graph.cypher.execute('CREATE CONSTRAINT ON (person:Person) ' \
                         'ASSERT person.uid IS UNIQUE')

@run.command()
def cleardb():
    '''Drop all data in the graph'''
    graph.delete_all()

if __name__ == '__main__':
    run()
