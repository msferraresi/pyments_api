import datetime
from flask import Blueprint, jsonify, request
from src.models.currency import CurrencySchema, Currency
from src import db

app = Blueprint('currency',__name__,url_prefix='/currency')

schema = CurrencySchema()
schemas = CurrencySchema(many=True)

@app.route('/create', methods=['POST'])
def create():
    values = request.get_json()           
    if not values:               
        return jsonify({'message': 'No input data provided'}), 400 # Bad request
    elif (values.get('name') is None):
        return jsonify({'message': 'No input data NAME provided'}), 400 # Bad request
    else: 
        if not (values.get('endpoint') is None):
            endpoint = values.get('endpoint')
        else:
            endpoint = ''
        element = Currency(values.get('name'), endpoint)
        db.session.add(element)
        db.session.commit()
        return jsonify({'data': schema.dump(element)}), 201 # Created}), 201

@app.route('/update/<id>', methods=['PUT'])
def update(id):
    element = Currency.query.get(id)
    values = request.get_json()  
    if not values:               
        return jsonify({'message': 'No input data provided'}), 400 # Bad request
    elif (values.get('name') is None):
        return jsonify({'message': 'No input data NAME provided'}), 400 # Bad request
    elif not element:               
        return jsonify({'message': 'No currency found'}), 404 # Not found
    else: 
        element.name = values.get('name')
        if not (values.get('endpoint') is None):
            element.endpoint = values.get('endpoint')
        db.session.commit()
        return jsonify({'data': schema.dump(element)}), 200 # OK

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    element = Currency.query.get(id)
    if not element:               
        return jsonify({'message': 'No currency found'}), 404 # Not found
    else: 
        element.deleted_at = datetime.datetime.now()
        db.session.commit()
        return jsonify({'message': 'Currency deleted'}), 200 # OK

@app.route('/all', methods=['GET'])
def list():
    elements = Currency.query.filter_by(deleted_at = None).all()
    if not elements:               
        return jsonify({'message': 'No currencies found'}), 404 # Not found
    else: 
        return jsonify({'data': schema.dump(elements, many=True)}), 200 # OK

@app.route('/get/<id>', methods=['GET'])
def getByID(id):
    element = Currency.query.get(id)
    if not element:               
        return jsonify({'message': 'No currency found'}), 404 # Not found
    else: 
        return jsonify({'data': schema.dump(element)}), 200 # OK