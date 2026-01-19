from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import Base, BaseModel

class Place(Base, BaseModel):
    __tablename__ = "places"
    title = Column(String(100), nullable = False)
    owner_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    description = Column(String(1024), default ="")
    price_per_night = Column(Float, default=0.0)
    
    owner = relationship("User" , back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
             "id": self.id,
             "title": self.title,
             "owner_id": self.owner_id,
             "description": self.description,
             "price_per_night": self.price_per_night,
             "created_at": self.created_at.isoformat() if self.created_at else None,
             "updated_at": self.updated_at.isoformat() if self.updated_at else None,
    }
