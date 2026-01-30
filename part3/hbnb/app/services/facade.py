from app.extensions import db

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

from app.repositories.user_repository import UserRepository
from app.repositories.place_repository import PlaceRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.amenity_repository import AmenityRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ======================
    # Users
    # ======================
    def create_user(self, email, password, first_name=None, last_name=None, is_admin=False):
        if not email or not password:
            raise ValueError("Email and password are required")

        existing = self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already exists")

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_admin=bool(is_admin),
        )
        user.set_password(password)
        return self.user_repo.add(user)

    # ======================
    # Places
    # ======================
    def create_place(self, place_data: dict):
        title = (place_data.get("title") or "").strip()
        if not title:
            raise ValueError("Title is required")

        owner_id = place_data.get("owner_id")
        owner = self.user_repo.get_by_id(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=title,
            description=(place_data.get("description") or ""),
            price_per_night=float(place_data.get("price_per_night") or 0.0),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner_id=owner_id,
        )
        return self.place_repo.add(place)

    def get_all_places(self):
        return self.place_repo.get_all()

    def get_place(self, place_id):
        return self.place_repo.get_by_id(place_id)

    # ======================
    # Reviews
    # ======================
    def create_review(self, review_data: dict):
        text = (review_data.get("text") or "").strip()
        if not text:
            raise ValueError("Review text is required")

        rating = review_data.get("rating")
        try:
            rating_int = int(rating)
        except (TypeError, ValueError):
            raise ValueError("Rating must be between 1 and 5")

        if not (1 <= rating_int <= 5):
            raise ValueError("Rating must be between 1 and 5")

        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise ValueError("Place not found")

        if place.owner_id == user_id:
            raise ValueError("You cannot review your own place")

        existing = self.review_repo.get_by_user_and_place(user_id, place_id)
        if existing:
            raise ValueError("You have already reviewed this place")

        review = Review(
            text=text,
            rating=rating_int,
            user_id=user_id,
            place_id=place_id,
        )

        return self.review_repo.add(review)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_review(self, review_id):
        return self.review_repo.get_by_id(review_id)

    # ======================
    # Amenities
    # ======================
    def create_amenity(self, amenity_data: dict):
        name = (amenity_data.get("name") or "").strip()
        if not name:
            raise ValueError("Amenity name is required")

        existing = self.amenity_repo.get_by_name(name)
        if existing:
            raise ValueError("Amenity already exists")

        amenity = Amenity(name=name)
        return self.amenity_repo.add(amenity)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get_by_id(amenity_id)

    def update_amenity(self, amenity_id, data: dict):
        amenity = self.amenity_repo.get_by_id(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        name = data.get("name")
        if name is not None:
            name = name.strip()
            if not name:
                raise ValueError("Amenity name is required")

            existing = self.amenity_repo.get_by_name(name)
            if existing and existing.id != amenity.id:
                raise ValueError("Amenity already exists")
            amenity.name = name

        db.session.commit()
        return amenity


facade = HBnBFacade()
