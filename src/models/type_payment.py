from src import db, ma

class TypePayment(db.Model):
    __tablename__ = 'type_payments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
                           
    def __init__(self, name):
        self.name = name
    
class TypePaymentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'created_at', 'updated_at', 'deleted_at')