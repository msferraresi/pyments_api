import os


class Config:
    ENV = "development"
    DEBUG = True
    TESTING = True
    SECRET_KEY = "dev"
    PORT_APP = 5001
    #SERVER_NAME = "localhost:5001"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USER_DB = "root"
    PASS_DB = "Lepo1867"
    HOST_DB = "localhost"
    PORT_DB = 3306
    NAME_DB = "pymentdb_prod"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{USER_DB}:{PASS_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}"
    )

    # Directorios necesarios
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    USER_FOLDER = "users"
    INVOICE_FOLDER = "invoices"
    RECEIPT_FOLDER = "receipts"
    HOUSE_FOLDER = "house"
