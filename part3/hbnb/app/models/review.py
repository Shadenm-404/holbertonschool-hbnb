from app.extensions import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    tablename = "reviews"

    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)

    table_args = (
        db.UniqueConstraint("user_id", "place_id", name="uq_review_user_place"),
        db.CheckConstraint("rating >= 1 AND rating <= 5", name="ck_review_rating_1_5"),
    )

    user = db.relationship("User", back_populates="reviews")
    place = db.relationship("Place", back_populates="reviews")

    def to_dict(self):
        return {
            "id": str(self.id),
            "text": self.text,
            "rating": self.rating,
            "user_id": str(self.user_id),
            "place_id": str(self.place_id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user": {
                "id": str(self.user.id),
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email
            }
    }
