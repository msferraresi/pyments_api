import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models.concept import ConceptSchema, Concept
from src import db

app = Blueprint("concept", __name__, url_prefix="/concept")

schema = ConceptSchema()


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

        concept = Concept(
            name=data["name"]
        )  # Crear el objeto Concept directamente con el diccionario
        db.session.add(concept)
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Concept created",
                    "data": schema.dump(concept),
                }
            ),
            201,
        )  # 201 Created

    except Exception as e:  # Capturar excepciones específicas si es posible
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred creating concept: {str(e)}",
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

        concept = Concept.query.filter_by(
            id=id, deleted_at=None
        ).first_or_404()  # Usar first_or_404()

        concept.name = data["name"]
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Concept updated",
                    "data": schema.dump(concept),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred updating concept: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        concept = Concept.query.filter_by(id=id, deleted_at=None).first_or_404()

        concept.deleted_at = dt.datetime.now()
        db.session.commit()
        return (
            jsonify({"status": "success", "message": "Concept deleted"}),
            200,
        )  # No es necesario enviar los datos borrados

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred deleting concept: {str(e)}",
                }
            ),
            500,
        )


@app.route("", methods=["GET"])
@jwt_required()
def list():
    try:
        concepts = (
            Concept.query.order_by(Concept.name.asc()).filter_by(deleted_at=None).all()
        )
        if not concepts:
            return (
                jsonify(
                    {"status": "success", "message": "No concepts found", "data": []}
                ),
                200,
            )  # 200 OK con lista vacía
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Concepts List",
                    "data": schema.dump(concepts, many=True),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting concepts: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_by_id(id):
    try:
        concept = Concept.query.get_or_404(id)  # Usar get_or_404()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Concept found",
                    "data": schema.dump(concept),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting concept: {str(e)}",
                }
            ),
            500,
        )
