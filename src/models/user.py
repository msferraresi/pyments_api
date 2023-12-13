from werkzeug.security import generate_password_hash, check_password_hash
from src import db, ma
from sqlalchemy.orm import relationship
from src.models import RoleSchema

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, default=2)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    roles = relationship("Role", back_populates='users')

    def __init__(self, name, last_name, password, mail, role_id):
        self.name = name
        self.last_name = last_name
        self.set_password(password)
        self.mail = mail
        self.role_id = role_id
        
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'mail': self.mail,
            'role_id': self.role_id,
            'role': {
                'id': self.roles.id,
                'name': self.roles.name
            }
        }
        
class UserSchema(ma.Schema):
    role = ma.Nested(RoleSchema, only=('id', 'name'))
    class Meta:
        model = User
        load_instance = True
        sqla_sesson = db.session
        fields = ('id', 'name', 'last_name', 'mail', 'role_id', 'role', 
                  'created_at', 'updated_at', 'deleted_at')