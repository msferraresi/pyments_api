import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models import TypeHouse, TypeHouseSchema
from src import db

app = Blueprint('type_house',__name__,url_prefix='/type_house')

schema = TypeHouseSchema()

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
            element = TypeHouse(values.get('name'))
            db.session.add(element)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Type house created', 'data': schema.dump(element)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred creating type house', 'data': {}}), 500

@app.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id=None):
    try:
        element = TypeHouse.query.filter_by(id=id, deleted_at=None).first()
        values = request.get_json()
        if not values:
            return jsonify({'status': 'error', 'message': 'No input data provided', 'data': {}}), 400 # Bad request
        elif values.get('name') is None:
            return jsonify({'status': 'error', 'message': 'No input data NAME provided', 'data': {}}), 400 # Bad request
        elif id is None:
            return jsonify({'status': 'error', 'message': 'No input data ID provided', 'data': {}}), 400 # Bad request
        elif not element:
            return jsonify({'status': 'error', 'message': 'Type house not found', 'data': {}}), 404 
        else:
            element.name = values.get('name')
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Type house updated', 'data': schema.dump(element)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred updating type house', 'data': {}}), 500

@app.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id=None):
    try:
        element = TypeHouse.query.filter_by(id=id, deleted_at=None).first()
        if id is None:               
            return jsonify({'status': 'error', 'message': 'No input data ID provided', 'data': {}}), 400 # Bad request
        elif not element:
            return jsonify({'status': 'error', 'message': 'Type house not found', 'data': {}}), 404 # Not Found
        else: 
            element.deleted_at = dt.datetime.now()
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Type house deleted', 'data': {}}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred deletenig type house', 'data': {}}), 500

@app.route('', methods=['GET'])
@jwt_required()
def list():
    try:
        elements = TypeHouse.query.order_by(TypeHouse.name.asc()).filter_by(deleted_at = None).all()
        if not elements:               
             return jsonify({'status': 'error', 'message': 'Type houses not found', 'data': []}), 404 # Not Found
        else: 
            return jsonify({'status': 'success', 'message': 'Type houses list', 'data': schema.dump(elements, many=True)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred geting type houses list', 'data': []}), 500

@app.route('/<int:id>', methods=['GET'])
@jwt_required()
def getByID(id):
    try:
        element = TypeHouse.query.get(id)
        if not element:               
             return jsonify({'status': 'error', 'message': 'Type house not found', 'data': {}}), 404 # Not Found
        else: 
            return jsonify({'status': 'success', 'message': 'Type house found', 'data': schema.dump(element)}), 200
    except:
      return jsonify({'status': 'error', 'message': 'An error occurred geting type house', 'data': {}}), 500