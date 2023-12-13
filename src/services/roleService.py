import datetime as dt
from flask import Blueprint, jsonify, request
from src.models import Role, RoleSchema
from src import db

app = Blueprint('role',__name__,url_prefix='/role')

schema = RoleSchema()
schemas = RoleSchema(many=True)
