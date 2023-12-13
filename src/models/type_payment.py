from src import db, ma
from sqlalchemy.orm import relationship
class TypePayment(db.Model):
    __tablename__ = 'type_payments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    payments = relationship('Payment', back_populates='type_payments')

    def __init__(self, name):
        self.name = name
    
class TypePaymentSchema(ma.Schema):
    class Meta:
        model = TypePayment
        load_instance = True
        sqla_sesson = db.session
        fields = ('id', 'name', 'created_at', 'updated_at', 'deleted_at')