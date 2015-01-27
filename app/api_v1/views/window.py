from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource
from app.api_v1.serializers import WindowSerializer
from app.models.Process import Window
from app.api_v1 import api
from app import db


class WindowView(Resource):
    def get(self, id):
        obj = Window.query.get_or_404(id)
        return WindowSerializer(obj).data

'''
    def delete(self, id):
        obj = Window.query.get_or_404(id)
        db.session.delete(obj)
        return '', 204

    def put(self, id):
        args = parser.parse_args()
        obj = {'window': args['window']}
        db.session.add(obj)
        return obj, 201
'''

class WindowViewList(Resource):
    def get(self):
        obj = Window.query.all()
        return {'windows': WindowSerializer(obj, many=True).data}
    '''
    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
    '''

api.add_resource(WindowViewList, '/window')
api.add_resource(WindowView, '/window/<id>')