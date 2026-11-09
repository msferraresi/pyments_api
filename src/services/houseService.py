import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models.house import HouseSchema, House  # Importar House

from src import db

app = Blueprint("house", __name__, url_prefix="/house")

schema = HouseSchema()


@app.route("", methods=["POST"])
@jwt_required()
def create():
    try:
        data = request.get_json()  # Usar 'data' en lugar de 'values'
        if not data:
            return (
                jsonify({"status": "error", "message": "No input data provided"}),
                400,
            )
        elif not data.get("name"):  # Simplificar la condición
            return jsonify({"status": "error", "message": "Name is required"}), 400
        elif not data.get("address"):
            return jsonify({"status": "error", "message": "Address is required"}), 400
        elif not data.get("number"):
            return jsonify({"status": "error", "message": "Number is required"}), 400
        elif not data.get("id_user"):
            return jsonify({"status": "error", "message": "User ID is required"}), 400
        elif not data.get("id_type_house"):
            return (
                jsonify({"status": "error", "message": "Type House ID is required"}),
                400,
            )

        house = House(
            name=data["name"],
            address=data["address"],
            number=data["number"],
            id_user=data["id_user"],
            id_type_house=data["id_type_house"],
        )
        db.session.add(house)
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "House created",
                    "data": schema.dump(house),
                }
            ),
            201,
        )  # 201 Created

    except Exception as e:  # Capturar excepciones específicas si es posible
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred creating house: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):  # No es necesario el valor por defecto en el argumento
    try:
        data = request.get_json()
        if not data:
            return (
                jsonify({"status": "error", "message": "No input data provided"}),
                400,
            )
        elif not data.get("name"):
            return jsonify({"status": "error", "message": "Name is required"}), 400
        elif not data.get("address"):
            return jsonify({"status": "error", "message": "Address is required"}), 400
        elif not data.get("number"):
            return jsonify({"status": "error", "message": "Number is required"}), 400
        elif not data.get("id_user"):
            return jsonify({"status": "error", "message": "User ID is required"}), 400
        elif not data.get("id_type_house"):
            return (
                jsonify({"status": "error", "message": "Type House ID is required"}),
                400,
            )

        house = House.query.filter_by(
            id=id, deleted_at=None
        ).first_or_404()  # Usar first_or_404()

        house.name = data["name"]
        house.address = data["address"]
        house.number = data["number"]
        house.id_user = data["id_user"]
        house.id_type_house = data["id_type_house"]

        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "House updated",
                    "data": schema.dump(house),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred updating house: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        house = House.query.filter_by(id=id, deleted_at=None).first_or_404()

        house.deleted_at = dt.datetime.now()
        db.session.commit()
        return (
            jsonify({"status": "success", "message": "House deleted"}),
            200,
        )  # No es necesario enviar los datos borrados

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred deleting house: {str(e)}",
                }
            ),
            500,
        )


@app.route("", methods=["GET"])
@jwt_required()
def list():
    try:
        houses = House.query.order_by(House.name.asc()).filter_by(deleted_at=None).all()
        if not houses:
            return (
                jsonify(
                    {"status": "success", "message": "No houses found", "data": []}
                ),
                200,
            )  # 200 OK con lista vacía
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Houses List",
                    "data": schema.dump(houses, many=True),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting houses: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_by_id(id):
    try:
        house = House.query.get_or_404(id)  # Usar get_or_404()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "House found",
                    "data": schema.dump(house),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting house: {str(e)}",
                }
            ),
            500,
        )
