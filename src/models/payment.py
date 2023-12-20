from src import db, ma
from sqlalchemy.orm import relationship
from src.models import StateSchema, TypePaymentSchema, CurrencySchema, ConceptSchema, HouseSchema
class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    id_status = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    id_type_payment = db.Column(db.Integer, db.ForeignKey('type_payments.id'), nullable=False)
    id_currency = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False)
    id_concept = db.Column(db.Integer, db.ForeignKey('concepts.id'), nullable=False)
    id_house = db.Column(db.Integer, db.ForeignKey('houses.id'), nullable=False)
    id_user = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    layer = db.Column(db.String(120), nullable=False)
    max_ammount = db.Column(db.Float, default=0, nullable=False)
    min_ammount = db.Column(db.Float, default=0, nullable=False)
    other_ammount = db.Column(db.Float, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    states = relationship("State", back_populates='payments')
    type_payments = relationship("TypePayment", back_populates='payments')
    currencies = relationship("Currency", back_populates='payments')
    concepts = relationship("Concept", back_populates='payments')
    houses = relationship("House", back_populates='payments')

    def __init__(self, id_status, id_type_payment, id_currency, id_concept, month, year, layer, max_ammount, min_ammount, other_ammount, id_house):
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
        self.id_house = id_house
        
    def to_dict(self):
        return {
            'id': self.id, 
            'id_status': self.id_status, 
            'id_type_payment': self.id_type_payment, 
            'id_currency': self.id_currency, 
            'id_concept': self.id_concept, 
            'month': self.month, 
            'year': self.year, 
            'layer': self.layer, 
            'max_ammount': self.max_ammount, 
            'min_ammount': self.min_ammount, 
            'other_ammount': self.other_ammount, 
            'status': {
                    'id': self.states.id,
                    'name': self.states.name,
                    },
            'type_payment': {
                    'id': self.type_payments.id,
                    'name': self.type_payments.name,
                    },
            'currency': {
                    'id': self.currencies.id,
                    'name': self.currencies.name,
                    },
            'concept': {
                    'id': self.concepts.id,
                    'name': self.concepts.name,
                    },
            'house': {
                    'id': self.houses.id,
                    'name': self.houses.name,
                    },
            'created_at': self.created_at, 
            'updated_at': self.updated_at, 
            'deleted_at': self.deleted_at
        }
    
class PaymentSchema(ma.Schema):
    states = ma.Nested(StateSchema, only=('id', 'name'))
    type_payments = ma.Nested(TypePaymentSchema, only=('id', 'name'))
    currencies = ma.Nested(CurrencySchema, only=('id', 'name'))
    concepts = ma.Nested(ConceptSchema, only=('id', 'name'))
    houses = ma.Nested(HouseSchema, only=('id', 'name'))
    class Meta:
        model = Payment
        load_instance = True
        sqla_sesson = db.session
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
                  'states', 'type_payments', 'currencies', 'concepts', 'houses', 'users',
                  'created_at', 
                  'updated_at', 
                  'deleted_at')