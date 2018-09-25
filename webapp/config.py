import os

#base directory
basedir = os.path.abspath(os.path.dirname(__file__))

#Base config for sqlit
class BaseConfig(object):
    SECRET_KEY = 'Fraunhofer is the best'
    DEBUG = True
    BCRPYT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False