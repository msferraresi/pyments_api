from collections import defaultdict
import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import and_, case, func
from src.models import PaymentSchema, Payment
from src import db
from sqlalchemy.orm import joinedload

app = Blueprint('payment', __name__, url_prefix='/payment')

schema = PaymentSchema()

# --------------------------------------------------Creacion----------------------------------------------------------------------
@app.route('', methods=['POST'])
@jwt_required()
def create():
    try:
        values = request.get_json()
        if not values:
            return jsonify({'status': 'error', 'message': 'No input data provided', 'data': {}}), 400 # Bad request
        elif values.get('id_status') is None:
            return jsonify({'status': 'error', 'message': 'No status provided', 'data': {}}), 400  # Bad request
        elif values.get('id_type_payment') is None:
            return jsonify({'status': 'error', 'message': 'No type payment provided', 'data': {}}), 400 # Bad request
        elif values.get('id_currency') is None:
            return jsonify({'status': 'error', 'message': 'No currency provided', 'data': {}}), 400  # Bad request
        elif values.get('id_concept') is None:
            return jsonify({'status': 'error', 'message': 'No concept provided', 'data': {}}), 400  # Bad request
        elif values.get('month') is None:
            return jsonify({'status': 'error', 'message': 'No month provided', 'data': {}}), 400  # Bad request
        elif values.get('year') is None:
            return jsonify({'status': 'error', 'message': 'No year provided', 'data': {}}), 400  # Bad request
        elif values.get('layer') is None or len(values.get('layer')) == 0:
            return jsonify({'status': 'error', 'message': 'No description provided', 'data': {}}), 400  # Bad request
        elif values.get('month') < 1 or values.get('month') > 12:
            return jsonify({'status': 'error', 'message': 'Month must be between 1 and 12', 'data': {}}), 400
        elif values.get('year') > dt.datetime.now().year:   
            return jsonify({'status': 'error', 'message': 'The year must be less than or equal to the current year', 'data': {}}), 400 # Bad request
        elif values.get('max_ammount') is None:
            return jsonify({'status': 'error', 'message': 'No max ammount provided', 'data': {}}), 400  # Bad request
        elif values.get('min_ammount') is None:
            return jsonify({'status': 'error', 'message': 'No min ammount provided', 'data': {}}), 400  # Bad request
        elif values.get('other_ammount') is None:
            return jsonify({'status': 'error', 'message': 'No other ammount provided', 'data': {}}), 400  # Bad request
        else:
            element = Payment(values.get('id_status'), values.get('id_type_payment'), values.get('id_currency'), values.get('id_concept'),
                                values.get('month'), values.get('year'), values.get('layer'), values.get('max_ammount'), values.get('min_ammount'), values.get('other_ammount'))
            db.session.add(element)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Payment created', 'data': schema.dump(element)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred creating payment', 'data': {}}), 500

# --------------------------------------------------Modificacion------------------------------------------------------------------


@app.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id=None):
    try:
        element = Payment.query.filter_by(id=id, deleted_at=None).first()
        values = request.get_json()
        if id is None:
            return jsonify({'status': 'error', 'message': 'No id provided', 'data': {}}), 400  # Bad
        if not element:
            return jsonify({'status': 'error', 'message': 'Payment not found', 'data': {}}), 404  # Bad
        if not values:
            return jsonify({'status': 'error', 'message': 'No input data provided', 'data': {}}), 400
        elif values.get('month') is None:
            return jsonify({'status': 'error', 'message': 'No month provided', 'data': {}}), 400  # Bad request
        elif values.get('year') is None:
            return jsonify({'status': 'error', 'message': 'No year provided', 'data': {}}), 400  # Bad request
        elif values.get('month') < 1 or values.get('month') > 12:
            return jsonify({'status': 'error', 'message': 'Month must be between 1 and 12', 'data': {}}), 400
        elif values.get('year') > dt.datetime.now().year:
            return jsonify({'status': 'error', 'message': 'The year must be less than or equal to the current year', 'data': {}}), 400
        else:
            element.id_status = values.get('id_status') if values.get('id_status') is not None else element.id_status
            element.id_type_payment = values.get('id_type_payment') if values.get('id_type_payment') is not None else element.id_type_payment
            element.id_currency = values.get('id_currency') if values.get('id_currency') is not None else element.id_currency
            element.id_concept = values.get('id_concept') if values.get('id_concept') is not None else element.id_concept
            element.month = values.get('month') if values.get('month') is not None else element.month
            element.year = values.get('year') if values.get('year') is not None else element.year
            element.layer = values.get('layer') if values.get('layer') is not None else element.layer
            element.max_ammount = values.get('max_ammount') if values.get('max_ammount') is not None else element.max_ammount
            element.min_ammount = values.get('min_ammount') if values.get('min_ammount') is not None else element.min_ammount
            element.other_ammount = values.get('other_ammount') if values.get('other_ammount') is not None else element.other_ammount
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Payment updated', 'data': schema.dump(element)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred updating payment', 'data': {}}), 500

# --------------------------------------------------Eliminacion-------------------------------------------------------------------


@app.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id=None):
    try:
        element = Payment.query.filter_by(id=id, deleted_at=None).first()
        if id is None:
            return jsonify({'status': 'error', 'message': 'No id provided', 'data': {}}), 400  # Bad
        if not element:
            return jsonify({'status': 'error', 'message': 'No payment found', 'data': {}}), 404  # Not found
        else:
            element.deleted_at = dt.datetime.now()
            db.session.commit()
        return jsonify({'status': 'success', 'message': 'Payment deleted', 'data': {}}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred deleting payment', 'data': {}}), 500


@app.route('/<int:month>/<int:year>', methods=['DELETE'])
@jwt_required()
def delete_all(month=None, year=None):
    try:
        elements = Payment.query.filter_by(year=year, month=month, deleted_at=None).all()
        if month is None:
            return jsonify({'status': 'error', 'message': 'No month provided', 'data': []}), 400  # Bad
        if year is None:
            return jsonify({'status': 'error', 'message': 'No year provided', 'data': []}), 400  # Bad
        if not elements:
            return jsonify({'status': 'error', 'message': 'Payments not found', 'data': []}), 404  # Not found
        else:
            for element in elements:
                element.deleted_at = dt.datetime.now()
            db.session.commit()
            return jsonify({'status': 'success', 'message': f'Payments deleted: {len(elements)}', 'data': []}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred deleting payments', 'data': []}), 500

    

# --------------------------------------------------Listados----------------------------------------------------------------------
@app.route('', methods=['GET'])
@jwt_required()
def get_all_payments_group_by_month2():
    try:
        elements = Payment.query\
                    .options(joinedload(Payment.states))\
                    .options(joinedload(Payment.type_payments))\
                    .order_by(Payment.year.desc(), Payment.month.desc())\
                    .filter_by(deleted_at = None).all()
        if not elements:
            return jsonify({'status': 'error', 'message': 'Payments not found', 'data': []}), 404  # Not found

        grouped_data = defaultdict(lambda: {'total_pagado': 0, 'total_adeudado': 0})

        for element in elements:
            # Determina qué columna usar para sumarizar
            column_to_sum = 0
            if element.type_payments.id == 1:
                column_to_sum = 'max_ammount'
            elif element.type_payments.id == 2:
                column_to_sum = 'min_ammount'
            else:
                column_to_sum = 'other_ammount'


            # Sumariza según el estado (pagado o adeudado)
            if element.states.id == 1:
                grouped_data[(element.year, element.month)]['total_pagado'] += getattr(element, column_to_sum)
            elif element.states.id == 2:
                grouped_data[(element.year, element.month)]['total_adeudado'] += getattr(element, column_to_sum)

        result = [{'total_pagado': data['total_pagado'],
                'total_adeudado': data['total_adeudado'],
                'month': month,
                'year': year}
                for (year, month), data in grouped_data.items()]

        return jsonify({'status': 'success', 'message': 'Payment List', 'data': result}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred getting the payments', 'data': []}), 500

@app.route('/<int:month>/<int:year>', methods=['GET'])
@jwt_required()
def list_payments_by_month_year(month=None, year=None):
    try:
        if year is None:
            return jsonify({'status': 'error', 'message': 'No year provided', 'data': []}), 400  # Bad request
        elif month is None:
            return jsonify({'status': 'error', 'message': 'No month provided', 'data': []}), 400  # Bad request
        else:
            elements = Payment.query.filter_by(year=year, month=month, deleted_at=None).all()
            if not elements:
                return jsonify({'status': 'error', 'message': 'No payments found', 'data': []}), 404
            else:
                return jsonify({'status': 'success', 'message': 'Payment List by month/year', 'data': schema.dump(elements, many=True)}), 200
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred getting month payments', 'data': []}), 500 # Internal server error

# --------------------------------------------------Obtener Uno---------------------------------------------------------------------

@app.route('/<int:id>', methods=['GET'])
@jwt_required()
def getByID(id=None):
    try:
        element = Payment.query.filter_by(id=id, deleted_at=None).first()
        if id is None:
            return jsonify({'status': 'error', 'message': 'No id provided', 'data': {}}), 400  # Bad request
        if not element:
            return jsonify({'status': 'error', 'message': 'Payment not found', 'data': {}}), 404  # Not found
        else:
            return jsonify({'status': 'success', 'message': 'Payment by id', 'data': schema.dump(element)}), 200  # OK
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred getting payment', 'data': {}}), 500 # Internal server error
