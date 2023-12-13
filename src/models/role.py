from src import db, ma
from sqlalchemy.orm import relationship

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
        
    users = relationship('User', back_populates='roles')

    def __init__(self, name):
        self.name = name
        
class RoleSchema(ma.Schema):
    class Meta:
        model = Role
        load_instance = True
        sqla_sesson = db.session
        fields = ('id', 'name', 'created_at', 'updated_at', 'deleted_at')