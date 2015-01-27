from flask import Blueprint
from flask.ext import restful
from flask.ext.principal import identity_loaded

api_v1 = Blueprint('api_v1', __name__)
api = restful.Api(api_v1)

from . import errors
from app.api_v1.views import session, user, process, window, post