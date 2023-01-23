import datetime
from flask import Blueprint, jsonify, request
from src.models.type_payment import TypePaymentSchema, TypePayment
from src import db

app = Blueprint('type_payment',__name__,url_prefix='/type_payment')

schema = TypePaymentSchema()
schemas = TypePaymentSchema(many=True)

@app.route('/create', methods=['POST'])
def create():
    values = request.get_json()           
    if not values:               
        return jsonify({'message': 'No input data provided'}), 400 # Bad request
    elif (values.get('name') is None):
        return jsonify({'message': 'No input data NAME provided'}), 400 # Bad request
    else: 
        element = TypePayment(values.get('name'))
        db.session.add(element)
        db.session.commit()
        return jsonify({'data': schema.dump(element)}), 201 # Created}), 201

@app.route('/update/<id>', methods=['PUT'])
def update(id):
    element = TypePayment.query.get(id)
    values = request.get_json()  
    if not values:               
        return jsonify({'message': 'No input data provided'}), 400 # Bad request
    elif (values.get('name') is None):
        return jsonify({'message': 'No input data NAME provided'}), 400 # Bad request
    elif not element:               
        return jsonify({'message': 'No type payment found'}), 404 # Not found
    else: 
        element.name = values.get('name')
        db.session.commit()
        return jsonify({'data': schema.dump(element)}), 200 # OK

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    element = TypePayment.query.get(id)
    if not element:               
        return jsonify({'message': 'No type payment found'}), 404 # Not found
    else: 
        element.deleted_at = datetime.datetime.now()
        db.session.commit()
        return jsonify({'message': 'Type payment deleted'}), 200 # OK

@app.route('/all', methods=['GET'])
def list():
    elements = TypePayment.query.order_by(TypePayment.name.asc()).filter_by(deleted_at = None).all()
    if not elements:               
        return jsonify({'message': 'No type payments found'}), 404 # Not found
    else: 
        return jsonify({'data': schema.dump(elements, many=True)}), 200 # OK


@app.route('/get/<id>', methods=['GET'])
def getByID(id):
    element = TypePayment.query.get(id)
    if not element:               
        return jsonify({'message': 'No type payment found'}), 404 # Not found
    else: 
        return jsonify({'data': schema.dump(element)}), 200 # OK