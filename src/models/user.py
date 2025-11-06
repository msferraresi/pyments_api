# user.py
from werkzeug.security import generate_password_hash, check_password_hash
from src import db, ma
from sqlalchemy.orm import relationship
from src.models.role import RoleSchema

# from src.models.house import HouseSchema


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=False)
    role_id = db.Column(
        db.Integer, db.ForeignKey("roles.id"), nullable=False, default=2
    )
    avatar_user = db.Column(db.String(200), default="default_user.png")
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # server_default
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )  # server_default y onupdate
    deleted_at = db.Column(db.DateTime, nullable=True)
    theme_brightness = db.Column(db.Integer, default=0)
    role = relationship("Role", back_populates="users")  # Singular: role
    houses = relationship("House", back_populates="user")  # Singular: user
    payments = db.relationship("Payment", back_populates="user")

    def __init__(
        self, name, last_name, password, mail, role_id, avatar_user, theme_brightness
    ):
        self.name = name
        self.last_name = last_name
        self.set_password(password)
        self.mail = mail
        self.role_id = role_id
        self.avatar_user = avatar_user
        self.theme_brightness = theme_brightness

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        role_data = {"id": self.role.id, "name": self.role.name} if self.role else None
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "mail": self.mail,
            "role_id": self.role_id,
            "role": role_data,
            "avatar_user": self.avatar_user,
            "theme_brightness": self.theme_brightness,
        }


class UserSchema(ma.Schema):
    role = ma.Nested(RoleSchema, only=("id", "name"))  # Singular: role
    # houses = ma.Nested(HouseSchema, only=("id", "name"))

    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session  # Corregido: sqla_session
        fields = (
            "id",
            "name",
            "last_name",
            "mail",
            "avatar_user",
            "role",
            # "houses",  # Singular: role
            "created_at",
            "updated_at",
            "deleted_at",
            "theme_brightness",
        )
