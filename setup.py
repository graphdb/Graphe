# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='Graphe',
    version='0.1.0',
    install_requires=[
        'Click==3.3',
        'py2neo==2.0.beta',
        'Flask==0.10.1',
        'Flask-Login==0.2.11',
        'Flask-OAuthlib==0.7.0'
    ],
    dependency_links=[
        'https://github.com/nigelsmall/py2neo/tarball/beta/2.0.tar.gz#egg=py2neo-2.0.beta'
    ]
)
