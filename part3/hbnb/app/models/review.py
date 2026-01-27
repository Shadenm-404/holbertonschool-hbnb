from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base_model import Base, BaseModel

class Review(Base, BaseModel):
    __tablename__ = "reviews"
    text 
        }
