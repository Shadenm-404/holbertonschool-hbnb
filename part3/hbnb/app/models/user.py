from app.extensions import db, bcrypt
from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship("Place", back_populates="owner", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
