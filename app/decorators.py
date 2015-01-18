from functools import wraps
from flask import abort
from flask.ext.login import current_user

from app.models.Permission import Permission

# A decorator is the things we can put on top of methods... for example, these guys above
# can be used as:
# >> @admin_required
# >> @permission_required(permission.permission)

# decorator created to be used when a view is called, but needs to verify if he has permission
# to see the entire view


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)