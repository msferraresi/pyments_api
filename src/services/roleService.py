from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.models.role import Role, RoleSchema

app = Blueprint("role", __name__, url_prefix="/role")

schema = RoleSchema()


@app.route("", methods=["GET"])
@jwt_required()
def list():
    try:
        roles = Role.query.order_by(Role.name.asc()).filter_by(deleted_at=None).all()
        if not roles:
            return (
                jsonify({"status": "success", "message": "No roles found", "data": []}),
                200,
            )  # 200 OK con lista vacía
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Roles List",
                    "data": schema.dump(roles, many=True),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting roles: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_by_id(id):
    try:
        role = Role.query.get_or_404(id)  # Usar get_or_404()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Role found",
                    "data": schema.dump(role),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting role: {str(e)}",
                }
            ),
            500,
        )
