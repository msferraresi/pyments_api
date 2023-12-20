import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models.currency import CurrencySchema, Currency
from src import db

app = Blueprint('currency',__name__,url_prefix='/currency')

schema = CurrencySchema()

@app.route('', methods=['POST'])
@jwt_required()
def create():
    try:
        values = request.get_json()           
        if not values:               
            return jsonify({'status': 'error', 'message': 'No input data provided', 'data': {}}), 400 # Bad request
        elif values.get('name') is None:
            return jsonify({'status': 'error', 'message': 'No input data NAME provided', 'data': {}}), 400 # Bad request
        else:
            if not (values.get('endpoint') is None):
                endpoint = values.get('endpoint')
            else:
                endpoint = ''
            element = Currency(values.get('name'), endpoint)
            db.session.add(element)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Currency created', 'data': schema.dump(element)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred creating currency', 'data': {}}), 500

@app.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id=None):
    try:
        element = Currency.query.filter_by(id=id, deleted_at=None).first()
        values = request.get_json()
        if not values:
            return jsonify({'status': 'error', 'message': 'No input data provided', 'data': {}}), 400 # Bad request
        elif values.get('name') is None:
            return jsonify({'status': 'error', 'message': 'No input data NAME provided', 'data': {}}), 400 # Bad request
        elif id is None:
            return jsonify({'status': 'error', 'message': 'No input data ID provided', 'data': {}}), 400 # Bad request
        elif not element:
            return jsonify({'status': 'error', 'message': 'Currency not found', 'data': {}}), 404 
        else:
            element.name = values.get('name')
            if not values.get('endpoint') is None:
                element.endpoint = values.get('endpoint')
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Currency updated', 'data': schema.dump(element)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred updating currency', 'data': {}}), 500

@app.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id=None):
    try:
        element = Currency.query.filter_by(id=id, deleted_at=None).first()
        if id is None:               
            return jsonify({'status': 'error', 'message': 'No input data ID provided', 'data': {}}), 400 # Bad request
        elif not element:
            return jsonify({'status': 'error', 'message': 'Currency not found', 'data': {}}), 404 # Not Found
        else: 
            element.deleted_at = dt.datetime.now()
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Currency deleted', 'data': {}}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred deletenig currency', 'data': {}}), 500

@app.route('', methods=['GET'])
@jwt_required()
def list():
    try:
        elements = Currency.query.order_by(Currency.name.asc()).filter_by(deleted_at = None).all()
        if not elements:               
             return jsonify({'status': 'error', 'message': 'Currencies not found', 'data': []}), 404 # Not Found
        else: 
            return jsonify({'status': 'success', 'message': 'Currencies List', 'data': schema.dump(elements, many=True)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred geting currencies list', 'data': []}), 500

@app.route('/<int:id>', methods=['GET'])
@jwt_required()
def getByID(id):
    try:
        element = Currency.query.get(id)
        if not element:               
             return jsonify({'status': 'error', 'message': 'Currency not found', 'data': {}}), 404 # Not Found
        else: 
            return jsonify({'status': 'success', 'message': 'Currency found', 'data': schema.dump(element)}), 200
    except:
      return jsonify({'status': 'error', 'message': 'An error occurred geting currency', 'data': {}}), 500