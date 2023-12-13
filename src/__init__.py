import os
from werkzeug.utils import find_modules, import_string
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

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
    jwt.init_app(app)
    CORS(app)
    

    with app.app_context():
        register_blueprint(app)
        db.create_all()
    
    with app.app_context():
        create_initial_data()

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    return app

def register_blueprint(app):
    for module in find_modules('src.services'):
        app.register_blueprint(import_string(module).app) 

def create_initial_data():
    from src.models import Concept, Currency, State, TypePayment, Role
    
    existing_data = Concept.query.all()
    if not existing_data:
        concepts = [
            Concept(name='Tarjeta Credito'),
            Concept(name='Telefonia'),
            Concept(name='Credito'),
            Concept(name='Servicio'),
            Concept(name='Impuesto'),
            Concept(name='Varios')
        ]

        db.session.add_all(concepts)
        db.session.commit()

    existing_data = Currency.query.all()
    if not existing_data:
        currencies = [
            Currency(name='Peso', endpoint=''),
            Currency(name='Dolar', endpoint=''),
            Currency(name='Euro', endpoint='')
        ]

        db.session.add_all(currencies)
        db.session.commit()
        
    existing_data = State.query.all()
    if not existing_data:
        states = [
            State(name='PAGADO'),
            State(name='ADEUDADO')
        ]

        db.session.add_all(states)
        db.session.commit()
        
    existing_data = TypePayment.query.all()
    if not existing_data:
        type_payments = [
            TypePayment(name='Total'),
            TypePayment(name='Minimo'),
            TypePayment(name='Otro')
        ]

        db.session.add_all(type_payments)
        db.session.commit()
    
    existing_data = Role.query.all()
    if not existing_data:
        roles = [
            Role(name='Empleado'),
            Role(name='Cliente')
        ]

        db.session.add_all(roles)
        db.session.commit()