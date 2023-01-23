import datetime
from flask import Blueprint, jsonify, request
from src.models.concept import ConceptSchema, Concept
from src import db

app = Blueprint('concept',__name__,url_prefix='/concept')

schema = ConceptSchema()
schemas = ConceptSchema(many=True)

@app.route('/create', methods=['POST'])
def create():
    values = request.get_json()           
    if not values:               
        return jsonify({'message': 'No input data provided'}), 400 # Bad request
    elif (values.get('name') is None):
        return jsonify({'message': 'No input data NAME provided'}), 400 # Bad request
    else: 
        element = Concept(values.get('name'))
        db.session.add(element)
        db.session.commit()
        return jsonify({'data': schema.dump(element)}), 201 # Created}), 201

@app.route('/update/<id>', methods=['PUT'])
def update(id):
    element = Concept.query.get(id)
    values = request.get_json()  
    if not values:               
        return jsonify({'message': 'No input data provided'}), 400 # Bad request
    elif (values.get('name') is None):
        return jsonify({'message': 'No input data NAME provided'}), 400 # Bad request
    elif not element:               
        return jsonify({'message': 'No concept found'}), 404 # Not found
    else: 
        element.name = values.get('name')
        db.session.commit()
        return jsonify({'data': schema.dump(element)}), 200 # OK

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    element = Concept.query.get(id)
    if not element:               
        return jsonify({'message': 'No state found'}), 404 # Not found
    else: 
        element.deleted_at = datetime.datetime.now()
        db.session.commit()
        return jsonify({'message': 'Concept deleted'}), 200 # OK

@app.route('/all', methods=['GET'])
def list():
    elements = Concept.query.order_by(Concept.name.asc()).filter_by(deleted_at = None).all()
    if not elements:               
        return jsonify({'message': 'No concepts found'}), 404 # Not found
    else: 
        return jsonify({'data': schema.dump(elements, many=True)}), 200 # OK

@app.route('/get/<id>', methods=['GET'])
def getByID(id):
    element = Concept.query.get(id)
    if not element:               
        return jsonify({'message': 'No concept found'}), 404 # Not found
    else: 
        return jsonify({'data': schema.dump(element)}), 200 # OK