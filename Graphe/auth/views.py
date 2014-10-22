# -*- coding: utf-8 -*-

from py2neo import Graph
from flask import redirect, request, session, url_for
from flask.ext.oauthlib.client import OAuth, OAuthException
from Graphe import app
from Graphe.models import graph
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
    if session.get('token.facebook'):
        return redirect(url_for('home'))

    callback = url_for(
        '.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return facebook.authorize(callback=callback)

@auth.route('/login/authorized')
def facebook_authorized():
    if session.get('token.facebook'):
        return redirect(url_for('home'))

    resp = facebook.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message

    # save token into session
    session['token.facebook'] = (resp['access_token'], '')

    # get user data from facebook
    me = facebook.get('/me')
    pic = facebook.get('/me/picture?redirect=0&type=large')

    # pick fields to save
    keys = ['id', 'name', 'first_name', 'middle_name', 'last_name',
            'email', 'gender', 'birthday', 'locale', 'relationship_status']
    data = {key: me.data[key] for key in keys if key in me.data}

    # rename id to uid
    data['uid'] = data.pop('id')

    # also pick user picture
    if not pic.data['data']['is_silhouette']:
        data['picture'] = pic.data['data']['url']

    # create user's node in graph
    person = graph.cypher.execute_one(
        'MERGE (person:Person { uid: { data }.uid }) ' \
        'ON CREATE SET person = { data } ' \
        'RETURN person',
        {'data': data}
    )

    friends = facebook.get('/me/friends')
    if friends.data['data']:
        for friend_data in friends.data['data']:
            friend = graph.cypher.execute_one(
                'MATCH (person:Person { uid: { data }.uid }) ' \
                'MERGE (friend:Person { uid: { friend }.id }) ' \
                'ON CREATE SET friend.name = { friend }.name ' \
                'MERGE person <- [rel:KNOWS] -> friend ' \
                'RETURN friend',
                {'data': data, 'friend': friend_data}
            )

    return redirect(url_for('home'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('token.facebook')
