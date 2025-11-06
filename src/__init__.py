import os
from werkzeug.utils import find_modules, import_string
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Inicialización de extensiones
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
config_data = ""


def create_app(environment=None):
    app_instance = Flask(__name__)

    if environment == "production":
        from config.production import Config as ProductionConfig

        app_instance.config.from_object(ProductionConfig)
    elif environment == "development":
        from config.development import Config as DevelopmentConfig

        app_instance.config.from_object(DevelopmentConfig)
    else:
        raise Exception("Ambiente no válido. Use 'development' o 'production'.")

    db.init_app(app_instance)
    ma.init_app(app_instance)
    jwt.init_app(app_instance)
    CORS(
        app_instance,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        origins=[
            "http://localhost:3000"
        ],  # Permite peticiones desde tu frontend de React
        supports_credentials=True,  # Permite el envío de cookies y headers de autorización
        allow_headers=["Authorization", "Content-Type"],
    )

    with app_instance.app_context():
        register_blueprint(app_instance)
        db.create_all()

    with app_instance.app_context():
        from src.models.concept import Concept
        from src.models.currency import Currency
        from src.models.status import Status
        from src.models.type_payment import TypePayment
        from src.models.role import Role
        from src.models.type_house import TypeHouse
        from src.models.user import User

        create_initial_data(
            Concept,
            [
                {"name": "Tarjeta Credito"},
                {"name": "Telefonia"},
                {"name": "Credito"},
                {"name": "Servicio"},
                {"name": "Impuesto"},
                {"name": "Varios"},
            ],
        )

        create_initial_data(
            Currency,
            [
                {"name": "Peso", "endpoint": ""},
                {"name": "Dolar", "endpoint": ""},
                {"name": "Euro", "endpoint": ""},
            ],
        )

        create_initial_data(
            Status, [{"name": "PAGADO"}, {"name": "ADEUDADO"}]
        )  # Usar Status

        create_initial_data(
            TypePayment, [{"name": "Total"}, {"name": "Minimo"}, {"name": "Otro"}]
        )

        create_initial_data(Role, [{"name": "Empleado"}, {"name": "Cliente"}])

        create_initial_data(
            TypeHouse,
            [
                {"name": "Principal"},
                {"name": "Laboral"},
                {"name": "Particular"},
                {"name": "Otra"},
            ],
        )
        create_initial_data(
            User,
            [
                {
                    "name": "Mauro",
                    "last_name": "Ferraresi",
                    "password": "Lepo1867",
                    "mail": "msferraresi@gmail.com",
                    "role_id": 1,
                    "avatar_user": None,
                    "theme_brightness": 0,
                }
            ],
        )

    create_subdirectory(
        app_instance.config["UPLOAD_FOLDER"], app_instance.config["USER_FOLDER"]
    )
    create_subdirectory(
        app_instance.config["UPLOAD_FOLDER"], app_instance.config["INVOICE_FOLDER"]
    )
    create_subdirectory(
        app_instance.config["UPLOAD_FOLDER"], app_instance.config["RECEIPT_FOLDER"]
    )
    create_subdirectory(
        app_instance.config["UPLOAD_FOLDER"], app_instance.config["HOUSE_FOLDER"]
    )

    global config_data
    config_data = app_instance
    return app_instance


def register_blueprint(app_instance):
    """Registra todos los blueprints de la carpeta services."""
    for module in find_modules("src.services"):
        app_instance.register_blueprint(import_string(module).app)


def create_subdirectory(base_folder, subdirectory):
    """Crea un subdirectorio dentro del directorio base si no existe."""
    if not os.path.exists(base_folder):
        os.makedirs(base_folder, exist_ok=True)

    subdirectory_path = os.path.join(base_folder, subdirectory)
    if not os.path.exists(subdirectory_path):
        os.makedirs(subdirectory_path, exist_ok=True)


def create_initial_data(model, values):
    """Inserta datos iniciales en la base de datos si no existen."""
    existing_data = model.query.all()
    if not existing_data:
        instances = [model(**value) for value in values]
        db.session.add_all(instances)
        db.session.commit()
