import datetime as dt
from flask import Blueprint, jsonify, request
from src.models import  HouseSchema
from src import db

app = Blueprint('house',__name__,url_prefix='/house')

schema = HouseSchema()