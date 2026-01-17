from sqlalchemy import Column, String, Boolean
from flask_bcrypt import Bcrypt

from app.models.base_model import Base, BaseModel

bcrypt = Bcrypt()


class User(BaseModel, Base):
    __tablename__ = "users"

    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    is_admin = Column(Boolean, default=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
