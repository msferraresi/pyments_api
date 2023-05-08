from distutils.debug import DEBUG
from sqlalchemy import true

class Config:
    ENV = None
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secret_key'
    PORT_APP = 5000
    SERVER_NAME = None
    SQLALCHEMY_TRACK_MODIFICATIONS=False


class DevelopmentConfig(Config):
    Config.ENV = 'development'
    Config.DEBUG = True
    Config.TESTING = True
    Config.SECRET_KEY = 'dev'
    Config.PORT_APP = 5001
    Config.SERVER_NAME = 'localhost:5001'
    USER_DB = 'root'
    PASS_DB = "Lepo_1867"
    HOST_DB = 'localhost'
    PORT_DB = 3306
    NAME_DB = 'pymentdb'
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USER_DB,PASS_DB,HOST_DB,PORT_DB,NAME_DB)