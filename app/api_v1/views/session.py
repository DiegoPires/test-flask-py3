#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
from flask import g, jsonify, current_app
from app.api_v1 import api
from app.models.Users import User
from app.models.AnonymousUser import AnonymousUser
from flask.ext.httpauth import HTTPBasicAuth
from app.api_v1.errors import unauthorized
from flask.ext.restful import reqparse, abort, Api, Resource
from flask.ext.principal import Principal, Identity, Permission, AnonymousIdentity, identity_changed, identity_loaded, RoleNeed, UserNeed, ActionNeed


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):

    if email_or_token == '':
        g.current_user = AnonymousUser()
        identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
        return True
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)

        g.token_used = True
        return g.current_user is not None
    else:
        g.token_used = False
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    identity_changed.send(current_app._get_current_object(),identity=Identity(g.current_user.roles))
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


class SessionView(Resource):
    @auth.login_required
    def get(self):
        if g.current_user.is_anonymous() or g.token_used:
            return unauthorized('Invalid credentials')
        return {'token': g.current_user.generate_auth_token(
            expiration=3600), 'expiration': 3600}


api.add_resource(SessionView, '/token')


