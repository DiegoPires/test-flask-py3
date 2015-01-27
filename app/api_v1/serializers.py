from datetime import date
from marshmallow import Schema, fields, pprint, Serializer

from bson import ObjectId
from marshmallow import Schema, fields

# Se encher o saco e tiver mtos id's, definir assim no schema evita de mapear
# como fields.String() toda a hora
#Schema.TYPE_MAPPING[ObjectId] = fields.String

class UserSerializer(Serializer):
    class Meta:
        fields = ("id", "email", "nickname")


class ProcessSerializer(Serializer):
    id = fields.String()

    class Meta:
        additional = ("created_at", "name")


class WindowSerializer(Serializer):
    process = fields.Nested(ProcessSerializer, only=('id', 'name'))

    class Meta:
        fields = ("id", "created_at", "title", "process")