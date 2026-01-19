from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base_model import Base, BaseModel

class Review(Base, BaseModel):
    __tablename__ = "reviews"
    text = Column(String(1000), nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(String(60), ForeignKey ("users.id"), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)

    __table_args__ = (
    UniqueConstraint("user_id","place_id", name = "uq_review_user_place"),
    )

    user = relationship("User", back_populates="reviews")
    place = relationship("Place", back_populates="reviews")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
