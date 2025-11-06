# payment.py
from src import db, ma
from sqlalchemy.orm import relationship
from src.models.status import StatusSchema
from src.models.type_payment import TypePaymentSchema
from src.models.currency import CurrencySchema
from src.models.concept import ConceptSchema
from src.models.house import HouseSchema
from src.models.user import UserSchema


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    id_status = db.Column(
        db.Integer, db.ForeignKey("statuses.id"), nullable=False
    )  # Referencia a statuses
    id_type_payment = db.Column(
        db.Integer, db.ForeignKey("type_payments.id"), nullable=False
    )
    id_currency = db.Column(db.Integer, db.ForeignKey("currencies.id"), nullable=False)
    id_concept = db.Column(db.Integer, db.ForeignKey("concepts.id"), nullable=False)
    id_house = db.Column(db.Integer, db.ForeignKey("houses.id"), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    layer = db.Column(db.String(120), nullable=False)
    max_ammount = db.Column(db.Float, default=0, nullable=False)
    min_ammount = db.Column(db.Float, default=0, nullable=False)
    other_ammount = db.Column(db.Float, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )
    deleted_at = db.Column(db.DateTime, nullable=True)

    status = relationship("Status", back_populates="payments")  # Referencia a Status
    type_payment = relationship("TypePayment", back_populates="payments")
    currency = relationship("Currency", back_populates="payments")
    concept = relationship("Concept", back_populates="payments")
    house = relationship("House", back_populates="payments")
    user = relationship("User", back_populates="payments")

    def __init__(
        self,
        id_status,
        id_type_payment,
        id_currency,
        id_concept,
        month,
        year,
        layer,
        max_ammount,
        min_ammount,
        other_ammount,
        id_house,
        id_user,
    ):
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
        self.id_user = id_user

    def to_dict(self):
        status_data = (
            {"id": self.status.id, "name": self.status.name} if self.status else None
        )
        type_payment_data = (
            {"id": self.type_payment.id, "name": self.type_payment.name}
            if self.type_payment
            else None
        )
        currency_data = (
            {"id": self.currency.id, "name": self.currency.name}
            if self.currency
            else None
        )
        concept_data = (
            {"id": self.concept.id, "name": self.concept.name} if self.concept else None
        )
        house_data = (
            {"id": self.house.id, "name": self.house.name} if self.house else None
        )
        user_data = {"id": self.user.id, "mail": self.user.mail} if self.user else None

        return {
            "id": self.id,
            "id_status": self.id_status,
            "id_type_payment": self.id_type_payment,
            "id_currency": self.id_currency,
            "id_concept": self.id_concept,
            "month": self.month,
            "year": self.year,
            "layer": self.layer,
            "max_ammount": self.max_ammount,
            "min_ammount": self.min_ammount,
            "other_ammount": self.other_ammount,
            "status": status_data,  # Clave 'status'
            "type_payment": type_payment_data,
            "currency": currency_data,
            "concept": concept_data,
            "house": house_data,
            "user": user_data,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }


class PaymentSchema(ma.Schema):
    status = ma.Nested(StatusSchema, only=("id", "name"))
    type_payment = ma.Nested(TypePaymentSchema, only=("id", "name"))
    currency = ma.Nested(CurrencySchema, only=("id", "name"))
    concept = ma.Nested(ConceptSchema, only=("id", "name"))
    house = ma.Nested(HouseSchema, only=("id", "name"))
    user = ma.Nested(UserSchema, only=("id", "mail"))

    class Meta:
        model = Payment
        load_instance = True
        sqla_session = db.session
        fields = (
            "id",
            "id_status",
            "id_type_payment",
            "id_currency",
            "id_concept",
            "month",
            "year",
            "layer",
            "max_ammount",
            "min_ammount",
            "other_ammount",
            "status",
            "type_payment",
            "currency",
            "concept",
            "house",
            "user",
            "created_at",
            "updated_at",
            "deleted_at",
        )
