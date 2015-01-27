from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from wtforms_alchemy import model_form_factory
from app import db
from app.models.Users import User


BaseModelForm = model_form_factory(Form)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class UserCreateForm(ModelForm):
    email = StringField('email', validators=[DataRequired()])
    nickname = StringField('nickname', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    #class Meta:
    #    model = User


class UserUpdateForm(ModelForm):
    email = StringField('email', validators=[DataRequired()])
    nickname = StringField('nickname', validators=[DataRequired()])


class SessionCreateForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class ProcessForm(Form):
    name = StringField('name', validators=[DataRequired()])