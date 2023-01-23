import datetime
from flask import Blueprint, jsonify, request
from src.models.state import StateSchema, State
from src import db

app = Blueprint('state',__name__,url_prefix='/state')

schema = StateSchema()
schemas = StateSchema(many=True)

@app.route('/create', methods=['POST'])
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

@app.route('/update/<id>', methods=['PUT'])
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

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    element = State.query.get(id)
    if not element:               
        return jsonify({'message': 'No state found'}), 404 # Not found
    else: 
        element.deleted_at = datetime.datetime.now()
        db.session.commit()
        return jsonify({'message': 'State deleted'}), 200 # OK

@app.route('/all', methods=['GET'])
def list():
    elements = State.query.order_by(State.name.asc()).filter_by(deleted_at = None).all()
    if not elements:               
        return jsonify({'message': 'No states found'}), 404 # Not found
    else: 
        return jsonify({'data': schema.dump(elements, many=True)}), 200 # OK

@app.route('/get/<id>', methods=['GET'])
def getByID(id):
    element = State.query.get(id)
    if not element:               
        return jsonify({'message': 'No state found'}), 404 # Not found
    else: 
        return jsonify({'data': schema.dump(element)}), 200 # OK