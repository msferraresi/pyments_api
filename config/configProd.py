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


class ProductionConfig(Config):
    Config.ENV = 'production'
    Config.DEBUG = False
    Config.TESTING = False
    Config.SECRET_KEY = 'prod'
    Config.PORT_APP = 5000
    Config.SERVER_NAME = 'localhost:5000'
    USER_DB = 'root'
    PASS_DB = 'Lepo#1867'
    HOST_DB = 'localhost'
    PORT_DB = 3306
    NAME_DB = 'pymentDB'
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USER_DB,PASS_DB,HOST_DB,PORT_DB,NAME_DB)