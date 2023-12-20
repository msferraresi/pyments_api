import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models.type_payment import TypePaymentSchema, TypePayment
from src import db

app = Blueprint('type_payment',__name__,url_prefix='/type_payment')

schema = TypePaymentSchema()

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
            element = TypePayment(values.get('name'))
            db.session.add(element)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Type payment created', 'data': schema.dump(element)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred creating type payment', 'data': {}}), 500

@app.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id=None):
    try:
        element = TypePayment.query.filter_by(id=id, deleted_at=None).first()
        values = request.get_json()
        if not values:
            return jsonify({'status': 'error', 'message': 'No input data provided', 'data': {}}), 400 # Bad request
        elif values.get('name') is None:
            return jsonify({'status': 'error', 'message': 'No input data NAME provided', 'data': {}}), 400 # Bad request
        elif id is None:
            return jsonify({'status': 'error', 'message': 'No input data ID provided', 'data': {}}), 400 # Bad request
        elif not element:
            return jsonify({'status': 'error', 'message': 'Type payment not found', 'data': {}}), 404 
        else:
            element.name = values.get('name')
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Type payment updated', 'data': schema.dump(element)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred updating type payment', 'data': {}}), 500

@app.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id=None):
    try:
        element = TypePayment.query.filter_by(id=id, deleted_at=None).first()
        if id is None:               
            return jsonify({'status': 'error', 'message': 'No input data ID provided', 'data': {}}), 400 # Bad request
        elif not element:
            return jsonify({'status': 'error', 'message': 'Type payment not found', 'data': {}}), 404 # Not Found
        else: 
            element.deleted_at = dt.datetime.now()
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Type payment deleted', 'data': {}}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred deletenig type payment', 'data': {}}), 500

@app.route('', methods=['GET'])
@jwt_required()
def list():
    try:
        elements = TypePayment.query.order_by(TypePayment.name.asc()).filter_by(deleted_at = None).all()
        if not elements:               
             return jsonify({'status': 'error', 'message': 'Type payments not found', 'data': []}), 404 # Not Found
        else: 
            return jsonify({'status': 'success', 'message': 'Type payments list', 'data': schema.dump(elements, many=True)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred geting type payments list', 'data': []}), 500

@app.route('/<int:id>', methods=['GET'])
@jwt_required()
def getByID(id):
    try:
        element = TypePayment.query.get(id)
        if not element:               
             return jsonify({'status': 'error', 'message': 'Type payment not found', 'data': {}}), 404 # Not Found
        else: 
            return jsonify({'status': 'success', 'message': 'Type payment found', 'data': schema.dump(element)}), 200
    except:
      return jsonify({'status': 'error', 'message': 'An error occurred geting type payment', 'data': {}}), 500