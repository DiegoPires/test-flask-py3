from flask import Flask, g, request
from flask.ext.restful import reqparse, abort, Api, Resource
from app.api_v1.forms import ProcessForm
from app.api_v1.serializers import ProcessSerializer, UserSerializer
from app.models.Process import Process
from app.api_v1 import api
from app.api_v1.views.session import auth
from app.roles import admin


class ProcessView(Resource):
    def get(self, id):
        process = Process.objects.get_or_404(id)
        return ProcessSerializer(process).data

    def delete(self, id):
        obj = Process.objects.get_or_404(id)
        obj.delete()
        return '', 204

    def put(self, id):
        form = ProcessForm()
        if not form.validate_on_submit():
            return form.errors, 422

        obj = Process.objects.get_or_404(id)
        obj.name = form.name.data

        obj.save()
        return ProcessSerializer(obj).data, 201


class ProcessViewList(Resource):
    @auth.login_required
    @admin.require(http_exception=403) #protect the whole method with the admin permission
    def get(self):
        # Or protect whatever you want to do whit the context, may work as a 'if' statement
        with admin.require():
            process = Process.objects.all()
            return {
                'process': ProcessSerializer(process, many=True).data,
            }
        unauthorized('Unauthorized')

    def post(self):
        form = ProcessForm()
        if not form.validate_on_submit():
            return form.errors, 422

        obj = Process(form.name.data)
        obj.save()
        return ProcessSerializer(obj).data





api.add_resource(ProcessViewList, '/process')
api.add_resource(ProcessView, '/process/<id>')