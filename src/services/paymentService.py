from collections import defaultdict
import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import and_, case, func
from src.models.payment import PaymentSchema, Payment
from src import db
from sqlalchemy.orm import joinedload

app = Blueprint("payment", __name__, url_prefix="/payment")

schema = PaymentSchema()


@app.route("", methods=["POST"])
@jwt_required()
def create():
    try:
        values = request.get_json()
        print(f"values: {values}")
        print(f"type(values): {type(values)}")
        if not values:
            return (
                jsonify({"status": "error", "message": "No input data provided"}),
                400,
            )  # Bad request
        elif values.get("id_status") is None:
            return (
                jsonify({"status": "error", "message": "Status is required"}),
                400,
            )  # Bad request
        elif values.get("id_type_payment") is None:
            return (
                jsonify({"status": "error", "message": "Type payment is required"}),
                400,
            )  # Bad request
        elif values.get("id_currency") is None:
            return (
                jsonify({"status": "error", "message": "Currency is required"}),
                400,
            )  # Bad request
        elif values.get("id_concept") is None:
            return (
                jsonify({"status": "error", "message": "Concept is required"}),
                400,
            )  # Bad request
        elif values.get("month") is None:
            return (
                jsonify({"status": "error", "message": "Month is required"}),
                400,
            )  # Bad request
        elif values.get("year") is None:
            return (
                jsonify({"status": "error", "message": "Year is required"}),
                400,
            )  # Bad request
        elif values.get("layer") is None or len(values.get("layer")) == 0:
            return (
                jsonify({"status": "error", "message": "Layer is required"}),
                400,
            )  # Bad request
        elif not 1 <= values.get("month") <= 12:  # Validar rango del mes
            return (
                jsonify(
                    {"status": "error", "message": "Month must be between 1 and 12"}
                ),
                400,
            )
        elif values.get("year") > dt.datetime.now().year:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Year must be less than or equal to the current year",
                    }
                ),
                400,
            )  # Bad request
        elif values.get("max_ammount") is None:
            return (
                jsonify({"status": "error", "message": "Max amount is required"}),
                400,
            )  # Bad request
        elif values.get("min_ammount") is None:
            return (
                jsonify({"status": "error", "message": "Min amount is required"}),
                400,
            )  # Bad request
        elif values.get("other_ammount") is None:
            return (
                jsonify({"status": "error", "message": "Other amount is required"}),
                400,
            )  # Bad request
        else:
            element = Payment(**values)  # Usar **values para pasar los datos
            db.session.add(element)
            db.session.commit()
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Payment created",
                        "data": schema.dump(element),
                    }
                ),
                201,
            )  # 201 Created

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred creating payment: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    try:
        payment = Payment.query.filter_by(
            id=id, deleted_at=None
        ).first_or_404()  # Simplificar la búsqueda y manejar 404
        values = request.get_json()

        if not values:
            return (
                jsonify({"status": "error", "message": "No input data provided"}),
                400,
            )
        elif (
            values.get("month") is not None and not 1 <= values.get("month") <= 12
        ):  # Validar rango del mes
            return (
                jsonify(
                    {"status": "error", "message": "Month must be between 1 and 12"}
                ),
                400,
            )
        elif (
            values.get("year") is not None
            and values.get("year") > dt.datetime.now().year
        ):
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Year must be less than or equal to the current year",
                    }
                ),
                400,
            )
        else:
            for (
                key,
                value,
            ) in values.items():  # Actualizar solo los campos proporcionados
                if hasattr(
                    payment, key
                ):  # Verificar si el atributo existe en el modelo
                    setattr(payment, key, value)

            db.session.commit()
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Payment updated",
                        "data": schema.dump(payment),
                    }
                ),
                200,
            )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred updating payment: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    try:
        payment = Payment.query.filter_by(id=id, deleted_at=None).first_or_404()
        payment.deleted_at = dt.datetime.now()
        db.session.commit()
        return jsonify({"status": "success", "message": "Payment deleted"}), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred deleting payment: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:month>/<int:year>", methods=["DELETE"])
@jwt_required()
def delete_all(month, year):  # No es necesario el valor por defecto None
    try:
        if not 1 <= month <= 12:
            return (
                jsonify(
                    {"status": "error", "message": "Month must be between 1 and 12"}
                ),
                400,
            )
        elif year > dt.datetime.now().year:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Year must be less than or equal to the current year",
                    }
                ),
                400,
            )

        payments = Payment.query.filter_by(
            year=year, month=month, deleted_at=None
        ).all()

        if not payments:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "No payments found for the specified month and year",
                    }
                ),
                404,
            )

        for payment in payments:
            payment.deleted_at = dt.datetime.now()

        db.session.commit()
        return (
            jsonify(
                {"status": "success", "message": f"Payments deleted: {len(payments)}"}
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred deleting payments: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id_house>", methods=["GET"])
@jwt_required()
def get_all_payments_group_by_month(id_house):
    # try:
    payments = (
        Payment.query.options(joinedload(Payment.status))
        .options(joinedload(Payment.type_payment))
        .order_by(Payment.year.desc(), Payment.month.desc())
        .filter_by(deleted_at=None, id_house=id_house)
        .all()
    )

    if not payments:
        return (
            jsonify({"status": "success", "message": "No payments found", "data": []}),
            200,
        )  # 200 OK si no hay pagos

    grouped_data = defaultdict(lambda: {"total_paid": 0, "total_due": 0})

    for payment in payments:
        # Determina qué columna usar para sumarizar
        amount_column = None
        if payment.type_payment.id == 1:
            amount_column = "max_ammount"
        elif payment.type_payment.id == 2:
            amount_column = "min_ammount"
        else:
            amount_column = "other_ammount"

        if amount_column is None:  # Manejar el caso de que no se encuentre la columna
            continue  # Saltar al siguiente pago

        amount = getattr(payment, amount_column)
        print(f"amount: {amount}")
        print(f"type(amount): {type(amount)}")
        print(f"payment.year: {payment.year}")
        print(f"payment.month: {payment.month}")
        print(f"payment.status.id: {payment.status.id}")

        # Sumariza según el estado (pagado o adeudado)
        if payment.status.id == 1:
            grouped_data[(payment.year, payment.month)]["total_paid"] += amount
        elif payment.status.id == 2:
            grouped_data[(payment.year, payment.month)]["total_due"] += amount

    result = [
        {
            "total_paid": data["total_paid"],
            "total_due": data["total_due"],
            "month": month,
            "year": year,
        }
        for (year, month), data in grouped_data.items()
    ]

    return (
        jsonify({"status": "success", "message": "Payment List", "data": result}),
        200,
    )

    # except Exception as e:
    #     return (
    #         jsonify(
    #             {
    #                 "status": "error",
    #                 "message": f"An error occurred getting the payments: {str(e)}",
    #             }
    #         ),
    #         500,
    #     )


@app.route("/<int:id_house>/<int:month>/<int:year>", methods=["GET"])
@jwt_required()
def list_payments_by_month_year(
    id_house, month, year
):  # No es necesario el valor por defecto None
    try:
        if not 1 <= month <= 12:
            return (
                jsonify(
                    {"status": "error", "message": "Month must be between 1 and 12"}
                ),
                400,
            )
        elif year > dt.datetime.now().year:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Year must be less than or equal to the current year",
                    }
                ),
                400,
            )

        payments = Payment.query.filter_by(
            year=year, month=month, deleted_at=None, id_house=id_house
        ).all()

        if not payments:
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "No payments found for the specified month and year",
                        "data": [],
                    }
                ),
                200,
            )  # 200 OK si no hay pagos

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Payment List by month/year",
                    "data": schema.dump(payments, many=True),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting month payments: {str(e)}",
                }
            ),
            500,
        )


@app.route("/<int:id>", methods=["GET"])
@jwt_required()
def getByID(id):  # No es necesario el valor por defecto None
    try:
        payment = Payment.query.filter_by(
            id=id, deleted_at=None
        ).first_or_404()  # Simplificar la búsqueda y manejar 404
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Payment by id",
                    "data": schema.dump(payment),
                }
            ),
            200,
        )  # OK

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred getting payment: {str(e)}",
                }
            ),
            500,
        )  # Internal server error


@app.route("/copy", methods=["POST"])
@jwt_required()
def copy_payments():
    try:
        data = request.get_json()
        if not data:
            return (
                jsonify({"status": "error", "message": "No input data provided"}),
                400,
            )

        # 1. Validación de campos requeridos
        required_fields = [
            "source_month",
            "source_year",
            "target_month",
            "target_year",
            "id_house",
            "id_user",
            "copy_amounts",
            "copy_payment_type",
        ]
        missing_fields = [field for field in required_fields if data.get(field) is None]
        if missing_fields:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"Missing required fields: {', '.join(missing_fields)}",
                    }
                ),
                400,
            )

        source_month = data["source_month"]
        source_year = data["source_year"]
        target_month = data["target_month"]
        target_year = data["target_year"]
        id_house = data["id_house"]
        id_user = data["id_user"]
        copy_amounts = data["copy_amounts"]
        copy_payment_type = data["copy_payment_type"]

        # 2. Buscar los pagos del mes de origen
        source_payments = Payment.query.filter_by(
            month=source_month,
            year=source_year,
            id_house=id_house,
            deleted_at=None,
        ).all()

        if not source_payments:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "No source payments found for the given month, year, and house.",
                    }
                ),
                404,
            )

        # 3. Prevenir duplicados en el mes de destino
        # existing_target_payments = Payment.query.filter_by(
        #     month=target_month, year=target_year, id_house=id_house, deleted_at=None
        # ).first()

        # if existing_target_payments:
        #     return (
        #         jsonify(
        #             {
        #                 "status": "error",
        #                 "message": "Payments already exist for the target month, year, and house. Cannot copy.",
        #             }
        #         ),
        #         409,  # Conflict
        #     )

        new_payments = []
        # 4. Crear los nuevos pagos
        for p in source_payments:
            new_payment = Payment(
                month=target_month,
                year=target_year,
                id_house=id_house,
                id_user=id_user,
                id_currency=p.id_currency,
                id_concept=p.id_concept,
                layer=p.layer,
                id_status=2,  # ADEUDADO
                max_ammount=p.max_ammount if copy_amounts else 0,
                min_ammount=p.min_ammount if copy_amounts else 0,
                other_ammount=p.other_ammount if copy_amounts else 0,
                id_type_payment=p.id_type_payment if copy_payment_type else 2,  # Minimo
            )
            new_payments.append(new_payment)

        # 5. Guardar en la base de datos
        if new_payments:
            db.session.add_all(new_payments)
            db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"{len(new_payments)} payments copied successfully to {target_month}/{target_year}.",
                    "data": schema.dump(new_payments, many=True),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An error occurred while copying payments: {str(e)}",
                }
            ),
            500,
        )
