from datetime import datetime
import os
from flask import Flask, render_template, flash, session, redirect, url_for
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Shell
from flask.ext.mail import Mail, Message

# the os is used the get the current path later used to create my sqlite db
basedir = os.path.abspath(os.path.dirname(__file__))

# Flask app
app = Flask(__name__)

# the manager for scritps
manager = Manager(app)

# other librarys
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)

#for crsf security
app.config['SECRET_KEY'] = 'quelque choose dificile a decouvrir'

#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#mail configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'dpires89@gmail.com'
app.config['FLASKY_ADMIN'] = 'dpires89@gmail.com'

# start my db with SQLAlchemy with migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# FORMS
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

# MODELS
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    email = db.Column(db.String(150), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username


# VIEWS
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


#@app.errorhandler(500)
#def internal_server_error(e):
#    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm(csrf_enabled=True)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                flash('email sent!')
                send_email(app.config['FLASKY_ADMIN'], 'New User',
                    'mail/new_user', user=user)
        else:
            session['known'] = True

        old_name = session.get('name')
        #if old_name is not None and old_name != form.name.data:
            #flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form,
                           name=session.get('name'),
                           known=session.get('known'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# email method
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
        sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


# Make Shell from manager works already importing those guys above
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

# runnning with the manager instead of app to accept params, like this it
# doens't work with Pycharm, because i'm not sending the 'runserver' parameter,
# PS, on configuration, it's possible to pass the required parameter
if __name__ == '__main__':
    manager.run()
