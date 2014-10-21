# -*- coding: utf-8 -*-

from flask import redirect, request, session, url_for
from flask.ext.oauthlib.client import OAuth, OAuthException
from Graphe import app
from . import auth

oauth = OAuth(app)

facebook = oauth.remote_app(
    'facebook',
    consumer_key=app.config['FACEBOOK_APP_ID'],
    consumer_secret=app.config['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email,user_likes,user_friends,user_relationships'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth'
)

@auth.route('/login')
def login():
    callback = url_for(
        '.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return facebook.authorize(callback=callback)

@auth.route('/login/authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message

    session['token.facebook'] = (resp['access_token'], '')
    me = facebook.get('/me')
    print me.data
    return redirect(url_for('home'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('token.facebook')
