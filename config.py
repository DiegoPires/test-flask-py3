import os
# the os is used the get the current path later used to create my sqlite db
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    #for crsf security
    SECRET_KEY = 'quelque choose dificile a decouvrir'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    #mail configuration
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'dpires89@gmail.com'
    FLASKY_ADMIN = 'dpires89@gmail.com'

    FLASKY_POSTS_PER_PAGE = 5
    FLASKY_FOLLOWERS_PER_PAGE = 5
    FLASKY_COMMENTS_PER_PAGE = 5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    MONGODB_SETTINGS = {'DB': "selfspy_db_dev"}


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    MONGODB_SETTINGS = {'DB': "selfspy_db_test"}


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    MONGODB_SETTINGS = {'DB': "selfspy_db"}



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}