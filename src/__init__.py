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
config_data = ''

def create_app(environment=None):
    app_instance = Flask(__name__)

    if environment == 'production':
        app_instance.config.from_object('config.configProd.ProductionConfig')
    elif environment == 'development':
        app_instance.config.from_object('config.configDev.DevelopmentConfig')
    else:
        raise(Exception)
    
    db.init_app(app_instance)
    ma.init_app(app_instance)
    jwt.init_app(app_instance)
    CORS(app_instance)
    

    with app_instance.app_context():
        register_blueprint(app_instance)
        db.create_all()
    
    '''with app.app_context():
        create_initial_data_old()'''
        
    with app_instance.app_context():
        from src.models import Concept, Currency, State, TypePayment, Role, TypeHouse
        create_initial_data(Concept, [
        {'name': 'Tarjeta Credito'},
        {'name': 'Telefonia'},
        {'name': 'Credito'},
        {'name': 'Servicio'},
        {'name': 'Impuesto'},
        {'name': 'Varios'}
        ])

        create_initial_data(Currency, [
            {'name': 'Peso', 'endpoint': ''},
            {'name': 'Dolar', 'endpoint': ''},
            {'name': 'Euro', 'endpoint': ''}
        ])

        create_initial_data(State, [
            {'name': 'PAGADO'},
            {'name': 'ADEUDADO'}
        ])

        create_initial_data(TypePayment, [
            {'name': 'Total'},
            {'name': 'Minimo'},
            {'name': 'Otro'}
        ])

        create_initial_data(Role, [
            {'name': 'Empleado'},
            {'name': 'Cliente'}
        ])

        create_initial_data(TypeHouse, [
            {'name': 'Principal'},
            {'name': 'Laboral'},
            {'name': 'Particular'},
            {'name': 'Otra'}
        ])
        
    create_subdirectory(app_instance.config['UPLOAD_FOLDER'], app_instance.config['USER_FOLDER'])
    create_subdirectory(app_instance.config['UPLOAD_FOLDER'], app_instance.config['INVOICE_FOLDER'])
    create_subdirectory(app_instance.config['UPLOAD_FOLDER'], app_instance.config['RECEIPT_FOLDER'])
    create_subdirectory(app_instance.config['UPLOAD_FOLDER'], app_instance.config['HOUSE_FOLDER'])
    global config_data
    config_data = app_instance
    #print(app_instance.config['UPLOAD_FOLDER'])
    return app_instance

def register_blueprint(app_instance):
    for module in find_modules('src.services'):
        app_instance.register_blueprint(import_string(module).app) 


def create_subdirectory(base_folder, subdirectory):
    if not os.path.exists(base_folder):
        os.makedirs(base_folder, exist_ok=True)
        
    subdirectory_path = os.path.join(base_folder, subdirectory)

    if not os.path.exists(subdirectory_path):
        os.makedirs(subdirectory_path, exist_ok=True)


def create_initial_data(model, values):
    existing_data = model.query.all()
    if not existing_data:
        instances = [model(**value) for value in values]
        db.session.add_all(instances)
        db.session.commit()



'''def create_initial_data_old():
    from src.models import Concept, Currency, State, TypePayment, Role
    #, TypeHouse
    
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
        
    existing_data = TypeHouse.query.all()
    if not existing_data:
        type_houses = [
            TypeHouse(name='Principal'),
            TypeHouse(name='Laboral'),
            TypeHouse(name='Particular'),
            TypeHouse(name='Otra')
        ]

        db.session.add_all(type_houses)
        db.session.commit()'''