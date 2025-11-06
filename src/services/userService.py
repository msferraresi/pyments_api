import base64
import datetime as dt
import os
from functools import wraps

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from src.models.user import User, UserSchema
from src import db
from src.utils.regex import Regex

app = Blueprint("user", __name__, url_prefix="/user")

schema = UserSchema()


def admin_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            target_user_id = kwargs.get("id")
            current_user_role = current_user_role_id()
            print(f"Current User ID: {current_user_id}, Type: {type(current_user_id)}")
            print(f"Target User ID: {target_user_id}, Type: {type(target_user_id)}")
            print(
                f"Current User Role: {current_user_role}, Type: {type(current_user_role)}"
            )

            if current_user_id and (
                current_user_id == str(target_user_id) or str(current_user_role) == "1"
            ):
                return fn(*args, **kwargs)
            else:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "Unauthorized access",
                            "data": {},
                        }
                    ),
                    403,
                )  # Not Found
        except:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "An error occurred validating user role",
                        "data": {},
                    }
                ),
                500,
            )

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
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "An error occurred getting current user role",
                    "data": {},
                }
            ),
            500,
        )


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        print(data)
        if (
            not data or not data.get("email") or not data.get("password")
        ):  # Validar que existan mail y password
            return (
                jsonify(
                    {"status": "error", "message": "Email and password are required"}
                ),
                400,
            )

        user = User.query.filter_by(mail=data["email"], deleted_at=None).first()

        from src import config_data

        image_path = f"{config_data.config['UPLOAD_FOLDER']}/{config_data.config['USER_FOLDER']}/{user.avatar_user}"

        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                image_content = image_file.read()
            image_base64 = base64.b64encode(image_content).decode("utf-8")
            image = image_base64
        else:
            image = "default_user.png"

        if user and user.check_password(data["password"]):
            user_id = user.id
            access_token = create_access_token(identity=str(user_id))
            refresh_token = create_refresh_token(identity=str(user_id))
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Login success",
                        "data": {
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                            "role": user.role.name,
                            "role_id": user.role.id,
                            "name": user.name,
                            "last_name": user.last_name,
                            "avatar_user": user.avatar_user,
                            "user_id": user.id,
                            "email": user.mail,
                            "image": image,
                            "theme_brightness": user.theme_brightness,
                        },
                    }
                ),
                200,
            )
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred during login: {str(e)}",
                }
            ),
            500,
        )


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        return (
            jsonify(
                {"status": "success", "access_token": new_access_token, "data": {}}
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred during token refresh: {str(e)}",
                }
            ),
            500,
        )


@app.route("", methods=["POST"])
def create():
    try:
        data = request.get_json()

        name = data.get("name")
        last_name = data.get("last_name")
        mail = data.get("email")
        password = data.get("password")
        re_password = data.get("re_password")
        role_id = data.get("role_id")

        if not name:
            return jsonify({"status": "error", "message": "Name is required"}), 400
        elif not last_name:
            return jsonify({"status": "error", "message": "Last name is required"}), 400
        elif not mail:
            return jsonify({"status": "error", "message": "Email is required"}), 400
        elif not Regex.check_email(mail):  # Validar el email con regex
            return jsonify({"status": "error", "message": "Invalid email format"}), 400
        elif not password:
            return jsonify({"status": "error", "message": "Password is required"}), 400
        elif password != re_password:
            return (
                jsonify({"status": "error", "message": "Passwords do not match"}),
                400,
            )
        elif not role_id:
            return jsonify({"status": "error", "message": "Role is required"}), 400

        avatar_user = "default_user.png"
        from src import config_data

        folder = (
            f"{config_data.config['UPLOAD_FOLDER']}/{config_data.config['USER_FOLDER']}"
        )
        if "photo" in request.files:
            photo_file = request.files["photo"]
            if photo_file.filename != "":
                avatar_user = photo_file.filename
                timestamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
                _, extension = os.path.splitext(photo_file.filename)
                filename = f"{timestamp}{extension}"
                filepath = os.path.join(folder, filename)
                photo_file.save(filepath)
                avatar_user = filename

        user = User(
            name=name,
            last_name=last_name,
            password=password,
            mail=mail,
            role_id=role_id,
            avatar_user=avatar_user,
            theme_brightness=0,
        )
        db.session.add(user)
        db.session.commit()

        user_data = schema.dump(user)
        image_path = f"{folder}/{user_data['avatar_user']}"
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                image_content = image_file.read()
            image_base64 = base64.b64encode(image_content).decode("utf-8")
            user_data["image"] = image_base64
        else:
            user_data["image"] = ""

        return (
            jsonify(
                {"status": "success", "message": "User created", "data": user_data}
            ),
            201,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred creating user: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["PUT"])
@jwt_required()
@admin_required
def update(id):
    try:
        # Verifica si el Content-Type es multipart/form-data
        if "multipart/form-data" not in request.content_type:
            # Si no es multipart, intenta procesar como JSON (esto es para ser más robusto)
            data = request.json
            name = data.get("name")
            last_name = data.get("last_name")
            role_id = data.get("role_id")
            avatar_user = data.get("avatar_user")
            photo_file = None
        else:
            # Si es multipart/form-data, procesa el formulario y los archivos
            name = request.form.get("name")
            last_name = request.form.get("last_name")
            role_id = request.form.get("role_id")
            avatar_user = request.form.get("avatar_user")
            photo_file = request.files.get("photo")

        if not name:
            return jsonify({"status": "error", "message": "Name is required"}), 400
        elif not last_name:
            return jsonify({"status": "error", "message": "Last name is required"}), 400
        elif not role_id:
            return jsonify({"status": "error", "message": "Role is required"}), 400

        user = User.query.filter_by(id=id, deleted_at=None).first_or_404()

        print(user.to_dict())
        photo_name = None
        if avatar_user != user.avatar_user:
            if avatar_user != "default_user.png":
                old_avatar_user = user.avatar_user
                from src import config_data

                folder = f"{config_data.config['UPLOAD_FOLDER']}/{config_data.config['USER_FOLDER']}"
                path_old_avatar_user = os.path.join(folder, old_avatar_user)
                if os.path.exists(path_old_avatar_user):
                    os.remove(path_old_avatar_user)

            if "photo" in request.files:
                photo_file = request.files["photo"]
                if photo_file.filename != "" and photo_file.filename is not None:
                    photo_name = photo_file.filename
                    timestamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
                    _, extension = os.path.splitext(photo_file.filename)
                    filename = f"{timestamp}{extension}"

                    filepath = os.path.join(folder, filename)
                    photo_file.save(filepath)
                    photo_name = filename
                    print(f"photo_name: {filename}")

        user.name = name if name is not None else user.name

        user.last_name = last_name if last_name is not None else user.last_name

        user.avatar_user = photo_name if photo_name is not None else user.avatar_user

        user.role_id = role_id if role_id is not None else user.role_id

        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "User updated",
                    "data": schema.dump(user),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred updating user: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete(id):
    try:
        user = User.query.filter_by(id=id, deleted_at=None).first_or_404()
        user.deleted_at = dt.datetime.now()
        db.session.commit()
        return jsonify({"status": "success", "message": "User deleted"}), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred deleting user: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["GET"])
@jwt_required()
@admin_required
def get_user_by_id(id):
    try:
        user = User.query.filter_by(
            id=id, deleted_at=None
        ).first_or_404()  # Simplificar la búsqueda y manejar 404
        user_data = schema.dump(user)

        from src import config_data

        image_path = f"{config_data.config['UPLOAD_FOLDER']}/{config_data.config['USER_FOLDER']}/{user_data['avatar_user']}"

        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                image_content = image_file.read()
            image_base64 = base64.b64encode(image_content).decode("utf-8")
            user_data["image"] = image_base64
        else:
            user_data["image"] = (
                "default_user.png"  # Opcional: asignar una imagen por defecto si no se encuentra
            )

        return (
            jsonify({"status": "success", "message": "User found", "data": user_data}),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting user: {str(e)}",
                }
            ),
            500,
        )


@app.route("", methods=["GET"])
@jwt_required()
@admin_required
def list_users():
    try:
        role_id = current_user_role_id()
        # Por seguridad, solo los administradores (role_id=1) deberían poder listar todos los usuarios.
        if role_id != 1:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Unauthorized access. Admin role required.",
                    }
                ),
                403,
            )

        users = User.query.order_by(User.name.asc()).filter_by(deleted_at=None).all()
        if not users:
            return (
                jsonify({"status": "success", "message": "No users found", "data": []}),
                200,
            )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Users list",
                    "data": schema.dump(users, many=True),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting users: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["PATCH"])
@jwt_required()
@admin_required
def update_password(id):
    try:
        old_password = request.form.get("old_password")
        password = request.form.get("password")
        re_password = request.form.get("re_password")

        print(f"old_password: {old_password}")
        print(f"password: {password}")
        print(f"re_password: {re_password}")

        user = User.query.filter_by(id=id, deleted_at=None).first_or_404()

        if not old_password:
            return (
                jsonify({"status": "error", "message": "Old password is required"}),
                400,
            )
        elif not password:
            return (
                jsonify({"status": "error", "message": "New password is required"}),
                400,
            )
        elif password != re_password:
            return (
                jsonify({"status": "error", "message": "Passwords do not match"}),
                400,
            )
        elif not user.check_password(old_password):
            return jsonify({"status": "error", "message": "Invalid old password"}), 401

        user.set_password(password)
        db.session.commit()
        return (
            jsonify({"status": "success", "message": "User password updated"}),
            200,
        )  # No es necesario enviar los datos actualizados

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred updating user password: {str(e)}",
                }
            ),
            500,
        )


@app.route("/setting/<int:id>", methods=["PATCH"])
@jwt_required()
@admin_required
def update_setting(id):
    try:
        theme_brightness = request.form.get("theme_brightness")

        user = User.query.filter_by(id=id, deleted_at=None).first_or_404()

        if not theme_brightness:
            return (
                jsonify({"status": "error", "message": "Brightness is required"}),
                400,
            )

        user.theme_brightness = theme_brightness
        db.session.commit()
        return (
            jsonify({"status": "success", "message": "User brightness updated"}),
            200,
        )  # No es necesario enviar los datos actualizados

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred updating user brightness: {str(e)}",
                }
            ),
            500,
        )
