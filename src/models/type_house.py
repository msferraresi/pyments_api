# type_house.py
from src import db, ma
from sqlalchemy.orm import relationship


class TypeHouse(db.Model):
    __tablename__ = "type_houses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )
    deleted_at = db.Column(db.DateTime, nullable=True)
    houses = relationship("House", back_populates="type_house")  # Singular: type_house

    def __init__(self, name):
        self.name = name


class TypeHouseSchema(ma.Schema):
    class Meta:
        model = TypeHouse
        load_instance = True
        sqla_session = db.session  # Corregido: sqla_session
        fields = ("id", "name", "created_at", "updated_at", "deleted_at")
