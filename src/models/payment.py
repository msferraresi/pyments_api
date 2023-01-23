from src import db, ma
from sqlalchemy.orm import relationship

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    id_status = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    id_type_payment = db.Column(db.Integer, db.ForeignKey('type_payments.id'), nullable=False)
    id_currency = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False)
    id_concept = db.Column(db.Integer, db.ForeignKey('concepts.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    layer = db.Column(db.String(120), nullable=False)
    max_ammount = db.Column(db.Float, default=0, nullable=False)
    min_ammount = db.Column(db.Float, default=0, nullable=False)
    other_ammount = db.Column(db.Float, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    status = relationship("State", foreign_keys=[id_status])
    type_payment = relationship("TypePayment", foreign_keys=[id_type_payment])
    currency = relationship("Currency", foreign_keys=[id_currency])
    concept = relationship("Concept", foreign_keys=[id_concept])


    def __init__(self, id_status, id_type_payment, id_currency, id_concept, month, year, layer, max_ammount, min_ammount, other_ammount):
        self.id_status = id_status
        self.id_type_payment = id_type_payment
        self.id_currency = id_currency
        self.id_concept = id_concept
        self.month = month
        self.year = year
        self.layer = layer
        self.max_ammount = max_ammount
        self.min_ammount = min_ammount
        self.other_ammount = other_ammount
    
class PaymentSchema(ma.Schema):
    class Meta:
        fields = ('id', 
                  'id_status', 
                  'id_type_payment', 
                  'id_currency', 
                  'id_concept', 
                  'month', 
                  'year', 
                  'layer', 
                  'max_ammount', 
                  'min_ammount', 
                  'other_ammount', 
                  'created_at', 
                  'updated_at', 
                  'deleted_at')

class PaymentSchema2(ma.Schema):
    class Meta:
        fields = ('month', 
                  'year',
                  'pagado',
                  'adeudado')

class PaymentSchema3(ma.Schema):
    class Meta:
        fields = ('id', 
                  'id_status',
                  'status.name',
                  'id_type_payment', 
                  'type_payment.name',
                  'id_currency', 
                  'currency.name',
                  'id_concept', 
                  'concept.name',
                  'month', 
                  'year', 
                  'layer', 
                  'max_ammount', 
                  'min_ammount', 
                  'other_ammount', 
                  'created_at', 
                  'updated_at', 
                  'deleted_at')