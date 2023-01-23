from werkzeug.utils import find_modules, import_string
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()

def create_app(environment=None):
    app = Flask(__name__)

    if environment == 'production':
        app.config.from_object('config.configProd.ProductionConfig')
    elif environment == 'development':
        app.config.from_object('config.configDev.DevelopmentConfig')
    else:
        raise(Exception)
    
    db.init_app(app)
    ma.init_app(app)
    

    with app.app_context():
        register_blueprint(app)
        db.create_all()

    return app

def register_blueprint(app):
    for module in find_modules('src.services'):
        app.register_blueprint(import_string(module).app) 