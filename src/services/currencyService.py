import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models.currency import CurrencySchema, Currency
from src import db

app = Blueprint("currency", __name__, url_prefix="/currency")

schema = CurrencySchema()


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

        endpoint = (
            data.get("endpoint") or ""
        )  # Valor por defecto vacío si no se proporciona

        currency = Currency(name=data["name"], endpoint=endpoint)
        db.session.add(currency)
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Currency created",
                    "data": schema.dump(currency),
                }
            ),
            201,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred creating currency: {str(e)}",
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

        currency = Currency.query.filter_by(id=id, deleted_at=None).first_or_404()

        currency.name = data["name"]
        currency.endpoint = (
            data.get("endpoint") or currency.endpoint
        )  # Mantener el valor anterior si no se proporciona uno nuevo

        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Currency updated",
                    "data": schema.dump(currency),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred updating currency: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        currency = Currency.query.filter_by(id=id, deleted_at=None).first_or_404()

        currency.deleted_at = dt.datetime.now()
        db.session.commit()
        return jsonify({"status": "success", "message": "Currency deleted"}), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred deleting currency: {str(e)}",
                }
            ),
            500,
        )


@app.route("", methods=["GET"])
@jwt_required()
def list():
    try:
        currencies = (
            Currency.query.order_by(Currency.name.asc())
            .filter_by(deleted_at=None)
            .all()
        )
        if not currencies:
            return (
                jsonify(
                    {"status": "success", "message": "No currencies found", "data": []}
                ),
                200,
            )
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Currencies List",
                    "data": schema.dump(currencies, many=True),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting currencies: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_by_id(id):
    try:
        currency = Currency.query.get_or_404(id)

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Currency found",
                    "data": schema.dump(currency),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting currency: {str(e)}",
                }
            ),
            500,
        )
