import base64
import datetime as dt
from functools import wraps
import os
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask import Blueprint, jsonify, request
from src.models import User, UserSchema
from src import db

app = Blueprint('user',__name__,url_prefix='/user')

schema = UserSchema()

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            target_user_id = kwargs.get('id')
            current_user_role = current_user_role_id()
            if current_user_id and (current_user_id == target_user_id or current_user_role == 1):      
                return fn(*args, **kwargs)
            else: 
                return jsonify({'status': 'error', 'message': 'Unauthorized access', 'data': {}}), 403 # Not Found
        except:
            return jsonify({'status': 'error', 'message': 'An error occurred validating user role', 'data': {}}), 500
    return wrapper

def current_user_role_id():
    try:
        current_user_id = get_jwt_identity()
        if current_user_id:
            user = User.query.get(current_user_id)
            return user.role_id if user else None
        else:
            return None
    except:
      return jsonify({'status': 'error', 'message': 'An error occurred getting current user role', 'data': {}}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        mail = data.get('mail')
        password = data.get('password')
        user = User.query.filter_by(mail=mail, deleted_at=None).first()
                
        if user and User.check_password(user, password):      
            access_token = create_access_token(identity=user.id)
            return jsonify({'status': 'success', 'message': 'Login success', 'data': {'access_token': access_token}}), 200
        else: 
            return jsonify({'status': 'error', 'message': 'Invalid credentials', 'data': {}}), 401 # Not Found
    except:
      return jsonify({'status': 'error', 'message': 'An error occurred login user', 'data': {}}), 500

@app.route('', methods=['POST'])
def create():
    try:
        name = request.form.get('name')
        last_name = request.form.get('last_name')
        mail = request.form.get('email')
        password = request.form.get('password')
        role_id = request.form.get('role_id')
        avatar_user = 'not_available.png'

        if name is None:
            return jsonify({'status': 'error', 'message': 'No input data NAME provided', 'data': {}}), 400 # Bad request
        elif last_name is None:
            return jsonify({'status': 'error', 'message': 'No input data LAST NAME provided', 'data': {}}), 400 # Bad request
        elif mail is None:
            return jsonify({'status': 'error', 'message': 'No input data EMAIL provided', 'data': {}}), 400 # Bad request
        elif password is None:
            return jsonify({'status': 'error', 'message': 'No input data PASSWORD provided', 'data': {}}), 400 # Bad request
        elif role_id is None:
            return jsonify({'status': 'error', 'message': 'No input data ROLE provided', 'data': {}}), 400 # Bad request
        else:
            if 'avatar_user' in request.file:
                photo_file = request.files['avatar_user']
                if photo_file.filename != '':
                    from src import config_data
                    folder = f"{config_data.config['UPLOAD_FOLDER']}/{config_data.config['USER_FOLDER']}"
                    avatar_user = photo_file.filename
                    timestamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
                    _, extension = os.path.splitext(photo_file.filename)
                    filename = f"{timestamp}{extension}"

                    filepath = os.path.join(folder, filename)
                    photo_file.save(filepath)
                    avatar_user = filename
            element = User(name=name, last_name=last_name, password=password, mail=mail, role_id=role_id, avatar_user=avatar_user)   
            db.session.add(element)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'User created', 'data': schema.dump(element)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred creating user', 'data': {}}), 500
    
@app.route('/<int:id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user_by_id(id):
    try:
        element = User.query.filter_by(id=id, deleted_at=None).first()
        if not element:               
             return jsonify({'status': 'error', 'message': 'User not found', 'data': {}}), 404 # Not Found
        else:
            user_data = schema.dump(element)
            from src import config_data
            image_path = f"{config_data.config['UPLOAD_FOLDER']}/{config_data.config['USER_FOLDER']}/{user_data['avatar_user']}"
            if os.path.exists(image_path):
                with open(image_path, 'rb') as image_file:
                    image_content = image_file.read()
                image_base64 = base64.b64encode(image_content).decode('utf-8')
                user_data['image'] = image_base64
            else:
                user_data['image'] = ''
        return jsonify({'status': 'success', 'message': 'User found', 'data': user_data}), 200
    except:
      return jsonify({'status': 'error', 'message': 'An error occurred geting user', 'data': {}}), 500
