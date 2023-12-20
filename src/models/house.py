from src import db, ma
from sqlalchemy.orm import relationship
from src.models import TypeHouseSchema

class House(db.Model):
    __tablename__ = 'houses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    id_type_house = db.Column(db.Integer, db.ForeignKey('type_houses.id'), nullable=False)
    avatar_house = db.Column(db.String(200), default='default_house.png') 
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
        
    payments = relationship('Payment', back_populates='houses')
    users = relationship('User', back_populates='houses')
    type_houses = relationship("TypeHouse", back_populates='houses')
    
    def __init__(self, name, address, number, id_user, id_type_house, avatar_house):
        self.name = name
        self.address = address
        self.number = number
        self.id_user = id_user
        self.id_type_house = id_type_house
        self.avatar_house = avatar_house
    
    def to_dict(self):
        return {'id': self.id, 
            'name': self.name, 
            'address': self.address, 
            'number': self.number, 
            'id_user': self.id_user, 
            'id_type_house': self.id_type_house, 
            'type_houses': {
                    'id': self.type_houses.id,
                    'name': self.type_houses.name,
                    },
            'user_owner': {
                    'id': self.users.id,
                    'name': self.users.mail,
                    },
            'avatar_house': self.avatar_house,
            'created_at': self.created_at, 
            'updated_at': self.updated_at, 
            'deleted_at': self.deleted_at}
        
class HouseSchema(ma.Schema):
    type_houses = ma.Nested(TypeHouseSchema, only=('id', 'name'))
    
    class Meta:
        model = House
        load_instance = True
        sqla_sesson = db.session
        fields = ('id', 'name', 'address', 'number', 'avatar_house', 'id_user', 'id_type_house', 'type_houses', 'users'
                  'created_at', 'updated_at', 'deleted_at')