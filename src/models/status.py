# status.py (antes state.py)
from src import db, ma
from sqlalchemy.orm import relationship


class Status(db.Model):  # Renombrado a Status
    __tablename__ = "statuses"  # Renombrado a statuses

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )
    deleted_at = db.Column(db.DateTime, nullable=True)

    payments = relationship("Payment", back_populates="status")  # Singular: status

    def __init__(self, name):
        self.name = name


class StatusSchema(ma.Schema):  # Renombrado a StatusSchema
    class Meta:
        model = Status  # Renombrado a Status
        load_instance = True
        sqla_session = db.session  # Corregido: sqla_session
        fields = ("id", "name", "created_at", "updated_at", "deleted_at")
