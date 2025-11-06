# house.py
from src import db, ma
from sqlalchemy.orm import relationship
from src.models.type_house import TypeHouseSchema
from src.models.user import UserSchema


class House(db.Model):
    __tablename__ = "houses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    id_type_house = db.Column(
        db.Integer, db.ForeignKey("type_houses.id"), nullable=False
    )
    avatar_house = db.Column(db.String(200), default="default_house.png")
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )
    deleted_at = db.Column(db.DateTime, nullable=True)

    payments = relationship("Payment", back_populates="house")  # Singular: house
    user = relationship("User", back_populates="houses")  # Singular: user
    type_house = relationship(
        "TypeHouse", back_populates="houses"
    )  # Singular: type_house

    def __init__(
        self, name, address, number, id_user, id_type_house
    ):  # Eliminar avatar_house
        self.name = name
        self.address = address
        self.number = number
        self.id_user = id_user
        self.id_type_house = id_type_house
        # self.avatar_house = avatar_house  # Se usa el valor por defecto del modelo

    def to_dict(self):
        type_house_data = (
            {"id": self.type_house.id, "name": self.type_house.name}
            if self.type_house
            else None
        )
        user_data = {"id": self.user.id, "mail": self.user.mail} if self.user else None
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "number": self.number,
            "id_user": self.id_user,
            "id_type_house": self.id_type_house,
            "type_house": type_house_data,
            "user_owner": user_data,
            "avatar_house": self.avatar_house,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }


class HouseSchema(ma.Schema):
    type_house = ma.Nested(TypeHouseSchema, only=("id", "name"))  # Singular: type_house
    user = ma.Nested(
        UserSchema, only=("id", "mail")
    )  # Incluir la información del usuario

    class Meta:
        model = House
        load_instance = True
        sqla_session = db.session  # Corregido: sqla_session
        fields = (
            "id",
            "name",
            "address",
            "number",
            "avatar_house",
            "id_user",
            "id_type_house",
            "type_house",
            "user",  # Corregido
            "created_at",
            "updated_at",
            "deleted_at",
        )
