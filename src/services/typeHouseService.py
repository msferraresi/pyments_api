import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models.type_house import TypeHouse, TypeHouseSchema
from src import db

app = Blueprint("type_house", __name__, url_prefix="/type_house")

schema = TypeHouseSchema()


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

        type_house = TypeHouse(name=data["name"])
        db.session.add(type_house)
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Type house created",
                    "data": schema.dump(type_house),
                }
            ),
            201,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred creating type house: {str(e)}",
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

        type_house = TypeHouse.query.filter_by(id=id, deleted_at=None).first_or_404()

        type_house.name = data["name"]
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Type house updated",
                    "data": schema.dump(type_house),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred updating type house: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        type_house = TypeHouse.query.filter_by(id=id, deleted_at=None).first_or_404()

        type_house.deleted_at = dt.datetime.now()
        db.session.commit()
        return jsonify({"status": "success", "message": "Type house deleted"}), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred deleting type house: {str(e)}",
                }
            ),
            500,
        )


@app.route("", methods=["GET"])
@jwt_required()
def list():
    try:
        type_houses = (
            TypeHouse.query.order_by(TypeHouse.name.asc())
            .filter_by(deleted_at=None)
            .all()
        )
        if not type_houses:
            return (
                jsonify(
                    {"status": "success", "message": "No type houses found", "data": []}
                ),
                200,
            )
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Type houses list",
                    "data": schema.dump(type_houses, many=True),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting type houses: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_by_id(id):
    try:
        type_house = TypeHouse.query.get_or_404(id)

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Type house found",
                    "data": schema.dump(type_house),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting type house: {str(e)}",
                }
            ),
            500,
        )
