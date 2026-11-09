import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models.status import StatusSchema, Status  # Importar Status y StatusSchema
from src import db

app = Blueprint("status", __name__, url_prefix="/status")  # Actualizar url_prefix

schema = StatusSchema()


@app.route("", methods=["POST"])
@jwt_required()
def create():
    try:
        data = request.get_json()
        if not data:
            return (
                jsonify({"status": "error", "message": "No input data provided"}),
                400,
            )
        elif not data.get("name"):
            return jsonify({"status": "error", "message": "Name is required"}), 400

        status = Status(name=data["name"])
        db.session.add(status)
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Status created",
                    "data": schema.dump(status),
                }
            ),
            201,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred creating status: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    try:
        data = request.get_json()
        if not data:
            return (
                jsonify({"status": "error", "message": "No input data provided"}),
                400,
            )
        elif not data.get("name"):
            return jsonify({"status": "error", "message": "Name is required"}), 400

        status = Status.query.filter_by(id=id, deleted_at=None).first_or_404()

        status.name = data["name"]
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Status updated",
                    "data": schema.dump(status),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred updating status: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        status = Status.query.filter_by(id=id, deleted_at=None).first_or_404()

        status.deleted_at = dt.datetime.now()
        db.session.commit()
        return jsonify({"status": "success", "message": "Status deleted"}), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred deleting status: {str(e)}",
                }
            ),
            500,
        )


@app.route("", methods=["GET"])
@jwt_required()
def list():
    try:
        statuses = (
            Status.query.order_by(Status.name.asc()).filter_by(deleted_at=None).all()
        )
        if not statuses:
            return (
                jsonify(
                    {"status": "success", "message": "No statuses found", "data": []}
                ),
                200,
            )
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Statuses List",
                    "data": schema.dump(statuses, many=True),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting statuses: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_by_id(id):
    try:
        status = Status.query.get_or_404(id)

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Status found",
                    "data": schema.dump(status),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting status: {str(e)}",
                }
            ),
            500,
        )
