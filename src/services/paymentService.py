import datetime
from flask import Blueprint, jsonify, request
from sqlalchemy import and_, case, func
from src.models.payment import PaymentSchema, PaymentSchema2, PaymentSchema3, Payment
from src import db

app = Blueprint('payment', __name__, url_prefix='/payment')

schema = PaymentSchema()
schemas = PaymentSchema(many=True)
schema2 = PaymentSchema2()
schemas2 = PaymentSchema2(many=True)
schema3 = PaymentSchema3()
schemas3 = PaymentSchema3(many=True)
# --------------------------------------------------Creacion----------------------------------------------------------------------


@app.route('/create', methods=['POST'])
def create():
    id_status = 0
    id_type_payment = 0
    id_currency = 0
    id_concept = 0
    month = 0
    year = 0
    layer = ''
    max_ammount = 0
    min_ammount = 0
    other_ammount = 0
    values = request.get_json()
    if not values:
        return jsonify({'message': 'No input data provided'}), 400 # Bad request
    elif (values.get('id_status') is None):
        return jsonify({'message': 'No status provided'}), 400  # Bad request
    elif (values.get('id_type_payment') is None):
        return jsonify({'message': 'No type payment provided'}), 400 # Bad request
    elif (values.get('id_currency') is None):
        return jsonify({'message': 'No currency provided'}), 400  # Bad request
    elif (values.get('id_concept') is None):
        return jsonify({'message': 'No concept provided'}), 400  # Bad request
    elif (values.get('month') is None):
        return jsonify({'message': 'No month provided'}), 400  # Bad request
    elif (values.get('year') is None):
        return jsonify({'message': 'No year provided'}), 400  # Bad request
    elif (values.get('layer') is None or len(values.get('layer')) is 0):
        return jsonify({'message': 'No description provided'}), 400  # Bad request
    elif (values.get('month') < 1 or values.get('month') > 12):
        return jsonify({'message': 'Month must be between 1 and 12'}), 400
    elif (values.get('year') > datetime.datetime.now().year):   
        return jsonify({'message': 'The year must be less than or equal to the current year'}), 400 # Bad request
    else:
        id_status = values.get('id_status')
        id_type_payment = values.get('id_type_payment')
        id_currency = values.get('id_currency')
        id_concept = values.get('id_concept')
        month = values.get('month')
        year = values.get('year')
        layer = values.get('layer')
        if not (values.get('max_ammount') is None):
            max_ammount = values.get('max_ammount')
        if not (values.get('min_ammount') is None):
            min_ammount = values.get('min_ammount')
        if not (values.get('other_ammount') is None):
            other_ammount = values.get('other_ammount')
        try:
            element = Payment(id_status, id_type_payment, id_currency, id_concept,
                              month, year, layer, max_ammount, min_ammount, other_ammount)
            db.session.add(element)
            db.session.commit()
            # Created}), 201
            return jsonify({'status': 'success', 'message': 'Payment created'}), 201
        except:
            # Internal server error
            return jsonify({'message': 'An error occurred creating the Payment'}), 500

# --------------------------------------------------Modificacion------------------------------------------------------------------


@app.route('/update/<id>', methods=['PUT'])
def update(id):
    element = Payment.query.get(id)
    if not element:
        return jsonify({'message': 'The element does not exist'}), 400  # Bad
    values = request.get_json()
    if not values:
        # Bad request
        return jsonify({'message': 'No input data provided'}), 400
    elif (values.get('month') is None):
        return jsonify({'message': 'No month provided'}), 400  # Bad request
    elif (values.get('year') is None):
        return jsonify({'message': 'No year provided'}), 400  # Bad request
    elif (values.get('month') < 1 or values.get('month') > 12):
        return jsonify({'message': 'Month must be between 1 and 12'}), 400
    elif (values.get('year') > datetime.datetime.now().year):
        # Bad request
        return jsonify({'message': 'The year must be less than or equal to the current year'}), 400
    else:
        if not (values.get('id_status') is None):
            element.id_status = values.get('id_status')
        if not (values.get('id_type_payment') is None):
            element.id_type_payment = values.get('id_type_payment')
        if not (values.get('id_currency') is None):
            element.id_currency = values.get('id_currency')
        if not (values.get('id_concept') is None):
            element.id_concept = values.get('id_concept')
        if not (values.get('month') is None):
            element.month = values.get('month')
        if not (values.get('year') is None):
            element.year = values.get('year')
        if not (values.get('layer') is None or len(values.get('layer')) is 0):
            element.layer = values.get('layer')
        if not (values.get('max_ammount') is None):
            element.max_ammount = values.get('max_ammount')
        if not (values.get('min_ammount') is None):
            element.min_ammount = values.get('min_ammount')
        if not (values.get('other_ammount') is None):
            element.other_ammount = values.get('other_ammount')
        try:
            db.session.commit()
            # Created}), 201
            return jsonify({'status': 'success', 'message': 'Payment updated'}), 201
        except:
            # Internal server error
            return jsonify({'message': 'An error occurred creating the Payment'}), 500

# --------------------------------------------------Eliminacion-------------------------------------------------------------------


@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    element = Payment.query.get(id)
    if not element:
        return jsonify({'message': 'No payment found'}), 404  # Not found
    else:
        element.deleted_at = datetime.datetime.now()
        db.session.commit()
        # OK
        return jsonify({'status': 'success', 'message': 'Payment deleted'}), 200


@app.route('/delete_all/<month>/<year>', methods=['DELETE'])
def delete_all(month, year):
    elements = Payment.query\
        .filter_by(year=year, month=month, deleted_at=None).all()
    if not elements:
        return jsonify({'message': 'No payments found'}), 404  # Not found
    else:
        # element.deleted_at = datetime.datetime.now()
        # db.session.commit()
        # OK
        return jsonify({'status': 'success', 'message': 'Payment deleted'}), 200

# --------------------------------------------------Listados----------------------------------------------------------------------


@app.route('/all', methods=['GET'])
def get_all_payments_group_by_month():
    try:
        elements = Payment.query.with_entities(Payment.month,
                                               Payment.year,
                                               func.sum(
                                                   case([(and_(Payment.id_status == 1, Payment.id_type_payment == 1), Payment.max_ammount),
                                                         (and_(Payment.id_status == 1, Payment.id_type_payment == 2), Payment.min_ammount),
                                                         (and_(Payment.id_status == 1, Payment.id_type_payment == 3), Payment.other_ammount)], 
                                                         else_ = 0)
                                               ).label('pagado'),
                                               func.sum(
                                                   case([(and_(Payment.id_status == 2, Payment.id_type_payment == 1), Payment.max_ammount),
                                                         (and_(Payment.id_status == 2, Payment.id_type_payment == 2), Payment.min_ammount),
                                                         (and_(Payment.id_status == 2, Payment.id_type_payment == 3), Payment.other_ammount)], 
                                                         else_ = 0)
                                               ).label('adeudado')
                                               ).filter_by(deleted_at = None).order_by(Payment.year.desc(), Payment.month.desc()).group_by(Payment.month, Payment.year).all()

        # OK
        return jsonify({'data': [schema2.dump(element) for element in elements]}), 200
    except:
        # Internal server error
        return jsonify({'message': 'An error occurred getting the Payments'}), 500


@app.route('/list/<month>/<year>', methods=['GET'])
def list_payments_by_month_year(month, year):
    if (year is None):
        return jsonify({'message': 'No year provided'}), 400  # Bad request
    elif (month is None):
        return jsonify({'message': 'No month provided'}), 400  # Bad request
    else:
        # try:
        elements = Payment.query\
            .filter_by(year=year, month=month, deleted_at=None).all()
        if not elements:
            return jsonify({'message': 'No payments found'}), 404
        else:
            # OK
            return jsonify({'data': [schema3.dump(element) for element in elements]}), 200
        # except:
     #   return jsonify({'message': 'An error occurred getting month payments'}), 500 # Internal server error

# --------------------------------------------------Obtener Uno---------------------------------------------------------------------


@app.route('/get/<id>', methods=['GET'])
def getByID(id):
    element = Payment.query.get(id)
    if not element:
        return jsonify({'message': 'No payment found'}), 404  # Not found
    else:
        return jsonify({'data': schema.dump(element)}), 200  # OK
