from src import db, ma
from sqlalchemy.orm import relationship
class Currency(db.Model):
    __tablename__ = 'currencies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    endpoint = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
        
    payments = relationship('Payment', back_populates='currencies')
    
    def __init__(self, name, endpoint):
        self.name = name
        self.endpoint = endpoint
        
class CurrencySchema(ma.Schema):
    class Meta:
        model = Currency
        load_instance = True
        sqla_sesson = db.session
        fields = ('id', 'name', 'endpoint', 'created_at', 'updated_at', 'deleted_at')