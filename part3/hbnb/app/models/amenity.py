from app.extensions import db
from app.models.base_model import BaseModel


class Place(BaseModel):
    tablename = "places"

    # Basic fields
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), default="")
    price_per_night = db.Column(db.Float, default=0.0, nullable=False)

    # Owner
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    # Relationships
    owner = db.relationship("User", back_populates="places")

    reviews = db.relationship(
        "Review",
        back_populates="place",
        cascade="all, delete-orphan"
    )

    amenities = db.relationship(
        "Amenity",
        secondary="place_amenity",
        back_populates="places"
    )

    def to_dict(self, include_amenities=True, include_reviews=False):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price_per_night": self.price_per_night,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_amenities:
            data["amenities"] = [
                {"id": a.id, "name": a.name} for a in (self.amenities or [])
            ]

        if include_reviews:
            data["reviews"] = [
                r.to_dict() for r in (self.reviews or [])
            ]

        return data
