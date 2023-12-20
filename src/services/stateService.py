import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models.state import StateSchema, State
from src import db

app = Blueprint('state',__name__,url_prefix='/state')

schema = StateSchema()

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
            element = State(values.get('name'))
            db.session.add(element)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'State created', 'data': schema.dump(element)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred creating state', 'data': {}}), 500

@app.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id=None):
    try:
        element = State.query.filter_by(id=id, deleted_at=None).first()
        values = request.get_json()
        if not values:
            return jsonify({'status': 'error', 'message': 'No input data provided', 'data': {}}), 400 # Bad request
        elif values.get('name') is None:
            return jsonify({'status': 'error', 'message': 'No input data NAME provided', 'data': {}}), 400 # Bad request
        elif id is None:
            return jsonify({'status': 'error', 'message': 'No input data ID provided', 'data': {}}), 400 # Bad request
        elif not element:
            return jsonify({'status': 'error', 'message': 'State not found', 'data': {}}), 404 
        else:
            element.name = values.get('name')
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'State updated', 'data': schema.dump(element)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred updating state', 'data': {}}), 500

@app.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id=None):
    try:
        element = State.query.filter_by(id=id, deleted_at=None).first()
        if id is None:               
            return jsonify({'status': 'error', 'message': 'No input data ID provided', 'data': {}}), 400 # Bad request
        elif not element:
            return jsonify({'status': 'error', 'message': 'State not found', 'data': {}}), 404 # Not Found
        else: 
            element.deleted_at = dt.datetime.now()
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'State deleted', 'data': {}}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred deletenig state', 'data': {}}), 500

@app.route('', methods=['GET'])
@jwt_required()
def list():
    try:
        elements = State.query.order_by(State.name.asc()).filter_by(deleted_at = None).all()
        if not elements:               
             return jsonify({'status': 'error', 'message': 'States not found', 'data': []}), 404 # Not Found
        else: 
            return jsonify({'status': 'success', 'message': 'States List', 'data': schema.dump(elements, many=True)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred geting states list', 'data': []}), 500

@app.route('/<int:id>', methods=['GET'])
@jwt_required()
def getByID(id):
    try:
        element = State.query.get(id)
        if not element:               
             return jsonify({'status': 'error', 'message': 'State not found', 'data': {}}), 404 # Not Found
        else: 
            return jsonify({'status': 'success', 'message': 'State found', 'data': schema.dump(element)}), 200
    except:
      return jsonify({'status': 'error', 'message': 'An error occurred geting state', 'data': {}}), 500