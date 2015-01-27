from flask.ext.restful import reqparse, abort, Api, Resource
from flask import request, jsonify
from app.api_v1 import api
from app import dbNoSql as db
from datetime import datetime
from marshmallow import Schema, fields, pprint, Serializer, ValidationError
from app.api_v1.errors import bad_request


class Post(db.Document):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    body = db.StringField(required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class CommentsSerializer(Serializer):
    class Meta:
        fields = ("created_at", "body", "author")


class PostSerializer(Serializer):
    id = fields.String()
    title = fields.String(required=True, validate=must_not_be_blank)
    comments = fields.Nested(CommentsSerializer, many=True)

    def make_object(self, data):
        return Post(**data)

    class Meta:
        additional = ("slug", "body", "created_at")


# just a test for multiple data
class PostViewList(Resource):
    def post(self):
        if not request.get_json():
            return bad_request('No input data provided')

        content_input = request.get_json().get("posts")

        serializer = PostSerializer(many=True)
        errors = serializer.validate(content_input)
        if errors:
            return jsonify(errors), 400
        result = serializer.load(content_input)
        r = Post.objects.insert(result.data)
        return PostSerializer(r, many=True).data, 201


api.add_resource(PostViewList, '/posts')