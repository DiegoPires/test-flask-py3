import os
from app import create_app, db
from app.models.User import User
from app.models.Role import Role
from app.models.Permission import Permission
from flask.ext.script import Manager, Shell
from flask.ext.migrate import MigrateCommand, Migrate


# create our app using the flask_config from system enviroment value or default
# to create the env var on Windows: SET FLASK_CONFIG = 'valor'
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


# method to define some default imports when runnning this file as shell:
# >> python manage.py shell
# or to do our migrations:
# >> python manage.py db init
# >> python manage.py db migrate -m 'comment'
# >> python manage.py db upgrade
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# decorator for a custom command for the Manager. The name of the
# method will be the name of the command
# >> python manage.py test
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

# main entry point
if __name__ == '__main__':
    manager.run()