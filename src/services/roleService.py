from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.models import Role, RoleSchema

app = Blueprint('role',__name__,url_prefix='/role')

schema = RoleSchema()

@app.route('', methods=['GET'])
@jwt_required()
def list():
    try:
        elements = Role.query.order_by(Role.name.asc()).filter_by(deleted_at = None).all()
        if not elements:               
             return jsonify({'status': 'error', 'message': 'Roles not found', 'data': []}), 404 # Not Found
        else: 
            return jsonify({'status': 'success', 'message': 'Roles List', 'data': schema.dump(elements, many=True)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred geting roles list', 'data': []}), 500

@app.route('/<int:id>', methods=['GET'])
@jwt_required()
def getByID(id):
    try:
        element = Role.query.get(id)
        if not element:               
             return jsonify({'status': 'error', 'message': 'Role not found', 'data': {}}), 404 # Not Found
        else: 
            return jsonify({'status': 'success', 'message': 'Role found', 'data': schema.dump(element)}), 200
    except:
      return jsonify({'status': 'error', 'message': 'An error occurred geting role', 'data': {}}), 500