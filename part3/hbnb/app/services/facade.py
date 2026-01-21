from app.db.session import SessionLocal
from app.repositories.user_repository import UserRepository
from app.repositories.place_repository import PlaceRepository
from app.repositories.review_repository import ReviewRepository 
from app.repositories.amenity_repository import AmenityRepository

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.session = SessionLocal()
        self.user_repo = UserRepository(self.session)
        self.place_repo = PlaceRepository(self.session)
        self.review_repo = ReviewRepository(self.session)
        self.amenity_repo = AmenityRepository(self.session)

    # ======================
    # Users
    # ======================
    def create_user(self, email, password, first_name=None, last_name=None):
        if not email or not password:
            raise ValueError("Email and password are required")

        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError("Email already exists")

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_admin=False
        )

        user.set_password(password)

        self.user_repo.add(user)

        return user

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    # ======================
    # Places
    # ======================
    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        user = self.user_repo.get_by_id(owner_id)
        if not user:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data["title"],
            owner_id=owner_id,
            description=place_data.get("description", ""),
            price_per_night=place_data.get("price_per_night", 0),
        )
        self.place_repo.add(place)
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def get_place(self, place_id):
        return self.place_repo.get_by_id(place_id)

    # ======================
    # Reviews
    # ======================
    def create_review(self, review_data):
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise ValueError("Place not found")

        existing = self.review_repo.get_by_user_and_place(user_id, place_id)
        if existing:
            raise ValueError("Review already exists for this user and place")

        review = Review(
            text=review_data["text"],
            user_id=user_id,
            place_id=place_id,
            rating=review_data.get("rating", 0),
        )
        self.review_repo.add(review)
        return review
    
    def get_all_reviews(self):
        return self.review_repo.get_all()
    
    def get_review(self, review_id):
        return self.review_repo.get_by_id(review_id)
    
    # ======================
    # Amenities      
    # ======================
def create_amenity(self, amenity_data):
    if "name" not in amenity_data or not amenity_data["name"]:
        raise ValueError("Amenity name is required")

    existing = self.amenity_repo.get_by_name(amenity_data["name"])
    if existing:
        raise ValueError("Amenity already exists")

    amenity = Amenity(name=amenity_data["name"])
    self.amenity_repo.add(amenity)
    return amenity


def get_all_amenities(self):
    return self.amenity_repo.get_all()


def get_amenity(self, amenity_id):
    amenity = self.amenity_repo.get_by_id(amenity_id)
    if not amenity:
        raise ValueError("Amenity not found")
    return amenity


def update_amenity(self, amenity_id, data):
    amenity = self.amenity_repo.get_by_id(amenity_id)
    if not amenity:
        raise ValueError("Amenity not found")

    if "name" in data and data["name"]:
        amenity.name = data["name"]

    self.session.commit()
    return amenity

facade = HBnBFacade()
