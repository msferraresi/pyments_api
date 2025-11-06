import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models.type_payment import TypePaymentSchema, TypePayment
from src import db

app = Blueprint("type_payment", __name__, url_prefix="/type_payment")

schema = TypePaymentSchema()


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

        type_payment = TypePayment(name=data["name"])
        db.session.add(type_payment)
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Type payment created",
                    "data": schema.dump(type_payment),
                }
            ),
            201,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred creating type payment: {str(e)}",
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

        type_payment = TypePayment.query.filter_by(
            id=id, deleted_at=None
        ).first_or_404()

        type_payment.name = data["name"]
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Type payment updated",
                    "data": schema.dump(type_payment),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred updating type payment: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        type_payment = TypePayment.query.filter_by(
            id=id, deleted_at=None
        ).first_or_404()

        type_payment.deleted_at = dt.datetime.now()
        db.session.commit()
        return jsonify({"status": "success", "message": "Type payment deleted"}), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred deleting type payment: {str(e)}",
                }
            ),
            500,
        )


@app.route("", methods=["GET"])
@jwt_required()
def list():
    try:
        type_payments = (
            TypePayment.query.order_by(TypePayment.name.asc())
            .filter_by(deleted_at=None)
            .all()
        )
        if not type_payments:
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "No type payments found",
                        "data": [],
                    }
                ),
                200,
            )
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Type payments list",
                    "data": schema.dump(type_payments, many=True),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting type payments: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_by_id(id):
    try:
        type_payment = TypePayment.query.get_or_404(id)

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Type payment found",
                    "data": schema.dump(type_payment),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting type payment: {str(e)}",
                }
            ),
            500,
        )
