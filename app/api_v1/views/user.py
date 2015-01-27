#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
from app import db
from app.api_v1.forms import UserCreateForm, UserUpdateForm
from app.api_v1.serializers import UserSerializer
from app.models.Users import User
from app.api_v1.errors import bad_request, unauthorized
from flask.ext.restful import reqparse, abort, Api, Resource
from app.api_v1 import api
from app.api_v1.views.session import auth
from app.roles import modifyUserPermission


class UserListView(Resource):
    # Deixei esse método sem autenticação pro cara poder se
    # cadastrar no sistema, por exemplo, novo usuário interessado, sei la?
    def post(self):
        form = UserCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User(email=form.email.data,
                    password=form.password.data,
                    nickname=form.nickname.data)
        db.session.add(user)
        db.session.commit()
        return UserSerializer(user).data

    @auth.login_required
    def get(self):
        users = User.query.all()
        return {'users': UserSerializer(users, many=True).data }


class UserView(Resource):
    @auth.login_required
    def get(self, id):
        obj = User.query.get_or_404(id)
        return UserSerializer(obj).data

    @auth.login_required
    def delete(self, id):
        obj = User.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return '', 204

    @auth.login_required
    def put(self, id):
        #permission = modifyUserPermission(id)
        #if permission.can():
        form = UserUpdateForm()
        if not form.validate_on_submit():
            return form.errors, 422 # Unprocessable Entity

        obj = User.query.get_or_404(id)
        obj.email = form.email.data
        obj.nickname = form.nickname.data

        db.session.add(obj)
        db.session.commit()
        return UserSerializer(obj).data, 201 # CREATED
        #unauthorized('Unauthorized')

api.add_resource(UserListView, '/user')
api.add_resource(UserView, '/user/<id>')