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
    values = request.get_json()           
    if not values:               
        return jsonify({'message': 'No input data provided'}), 400 # Bad request
    elif (values.get('name') is None):
        return jsonify({'message': 'No input data NAME provided'}), 400 # Bad request
    else: 
        element = State(values.get('name'))
        db.session.add(element)
        db.session.commit()
        return jsonify({'data': schema.dump(element)}), 201 # Created}), 201

@app.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    element = State.query.get(id)
    values = request.get_json()  
    if not values:               
        return jsonify({'message': 'No input data provided'}), 400 # Bad request
    elif (values.get('name') is None):
        return jsonify({'message': 'No input data NAME provided'}), 400 # Bad request
    elif not element:               
        return jsonify({'message': 'No state found'}), 404 # Not found
    else: 
        element.name = values.get('name')
        db.session.commit()
        return jsonify({'data': schema.dump(element)}), 200 # OK

@app.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    element = State.query.get(id)
    if not element:               
        return jsonify({'message': 'No state found'}), 404 # Not found
    else: 
        element.deleted_at = datetime.datetime.now()
        db.session.commit()
        return jsonify({'message': 'State deleted'}), 200 # OK

@app.route('', methods=['GET'])
@jwt_required()
def list():
    elements = State.query.order_by(State.name.asc()).filter_by(deleted_at = None).all()
    if not elements:               
        return jsonify({'message': 'No states found'}), 404 # Not found
    else: 
        return jsonify({'data': schema.dump(elements, many=True)}), 200 # OK

@app.route('/<int:id>', methods=['GET'])
@jwt_required()
def getByID(id):
    element = State.query.get(id)
    if not element:               
        return jsonify({'message': 'No state found'}), 404 # Not found
    else: 
        return jsonify({'data': schema.dump(element)}), 200 # OK