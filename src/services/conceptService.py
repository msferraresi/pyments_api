import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models.concept import ConceptSchema, Concept
from src import db

app = Blueprint('concept',__name__,url_prefix='/concept')

schema = ConceptSchema()

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
            element = Concept(values.get('name'))
            db.session.add(element)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Concept created', 'data': schema.dump(element)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred creating concept', 'data': {}}), 500

@app.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id=None):
    try:
        element = Concept.query.filter_by(id=id, deleted_at=None).first()
        values = request.get_json()
        if not values:
            return jsonify({'status': 'error', 'message': 'No input data provided', 'data': {}}), 400 # Bad request
        elif values.get('name') is None:
            return jsonify({'status': 'error', 'message': 'No input data NAME provided', 'data': {}}), 400 # Bad request
        elif id is None:
            return jsonify({'status': 'error', 'message': 'No input data ID provided', 'data': {}}), 400 # Bad request
        elif not element:
            return jsonify({'status': 'error', 'message': 'Concept not found', 'data': {}}), 404 
        else:
            element.name = values.get('name')
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Concept updated', 'data': schema.dump(element)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred updating concept', 'data': {}}), 500

@app.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id=None):
    try:
        element = Concept.query.filter_by(id=id, deleted_at=None).first()
        if id is None:               
            return jsonify({'status': 'error', 'message': 'No input data ID provided', 'data': {}}), 400 # Bad request
        elif not element:
            return jsonify({'status': 'error', 'message': 'Concept not found', 'data': {}}), 404 # Not Found
        else: 
            element.deleted_at = dt.datetime.now()
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Concept deleted', 'data': {}}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred deletenig concept', 'data': {}}), 500

@app.route('', methods=['GET'])
@jwt_required()
def list():
    try:
        elements = Concept.query.order_by(Concept.name.asc()).filter_by(deleted_at = None).all()
        if not elements:               
             return jsonify({'status': 'error', 'message': 'Concepts not found', 'data': []}), 404 # Not Found
        else: 
            return jsonify({'status': 'success', 'message': 'Concepts List', 'data': schema.dump(elements, many=True)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred geting concepts list', 'data': []}), 500

@app.route('/<int:id>', methods=['GET'])
@jwt_required()
def getByID(id):
    try:
        element = Concept.query.get(id)
        if not element:               
             return jsonify({'status': 'error', 'message': 'Concept not found', 'data': {}}), 404 # Not Found
        else: 
            return jsonify({'status': 'success', 'message': 'Concept found', 'data': schema.dump(element)}), 200
    except:
      return jsonify({'status': 'error', 'message': 'An error occurred geting concept', 'data': {}}), 500