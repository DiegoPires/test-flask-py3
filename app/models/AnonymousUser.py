from flask.ext.login import AnonymousUserMixin


# Class implement so when the current_user is called from the flask-login is initialized
# with it, so it's not necessary to verify is the current_user is logged or not, its
# already and 'anonymoususer'
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False