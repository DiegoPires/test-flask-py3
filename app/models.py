# MODELS
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask.ext.login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


# Herdando o UserMixin, uma classe do flask-login que ja implementa os métodos:
# >> is_authenticated(), is_active(), is_anonymous(), get_id()
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    # REMOVE ON PROD, just using it here because my email dont work
    token = db.Column(db.String(200))

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # methods used to set our hashed password, make it readonly and compare a given one
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # method used for Flask-login as a callback to load an user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # methods to use with the token generated when a user is created
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def __repr__(self):
        return '<User %r>' % self.username