import datetime as dt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask import Blueprint, jsonify, request
from src.models import User, UserSchema
from src import db

app = Blueprint('user',__name__,url_prefix='/user')

schema = UserSchema()
schemas = UserSchema(many=True)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Obtén las credenciales del cuerpo de la solicitud
    mail = data.get('mail')
    password = data.get('password')

    # Autentica al usuario (deberías implementar tu propia lógica de autenticación)
    user = User.query.filter_by(mail=mail).first()
    print(f"Usuario BD: {user.password}")
    print(f"Password PAYLOAD: {password}")
    if user and User.check_password(user, password):
        access_token = create_access_token(identity=mail)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

@app.route('', methods=['POST'])
def create():
    values = request.get_json()
    if not values:
        return jsonify({'message': 'No input data provided'}), 400 # Bad request
    elif values.get('name') is None:
        return jsonify({'message': 'No input data NAME provided'}), 400 # Bad request
    elif values.get('last_name') is None:
        return jsonify({'message': 'No input data LAST NAME provided'}), 400 # Bad request
    elif values.get('email') is None:
        return jsonify({'message': 'No input data EMAIL provided'}), 400 # Bad request
    elif values.get('password') is None:
        return jsonify({'message': 'No input data PASSWORD provided'}), 400 # Bad request
    elif values.get('role_id') is None:
        return jsonify({'message': 'No input data ROLE provided'}), 400 # Bad request
    else:
        try:
            element = User(values.get('name'), values.get('last_name'), values.get('password'), values.get('email'), values.get('role_id'))
            db.session.add(element)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'User created'}), 201
        except:
            return jsonify({'message': 'An error occurred creating User'}), 500

@app.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    current_user_id = get_jwt_identity()

    # Verifica si el usuario autenticado tiene permiso para obtener el perfil de otro usuario
    #if current_user_id != user_id:
    #    return jsonify({"error": "No tienes permisos para acceder a este recurso"}), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(user.to_dict()), 200