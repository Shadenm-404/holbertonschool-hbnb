from app.repositories.in_memory_repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ======================
    # Users
    # ======================
    def create_user(self, user_data):
        existing_users = self.user_repo.get_all()
        for user in existing_users:
            if user.email == user_data.get('email'):
                raise ValueError("User with this email already exists")

        if 'email' not in user_data:
            raise ValueError("Email is required")

        user = User(
            email=user_data['email'],
            password=user_data.get('password', ''),
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', '')
        )
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
        owner_id = place_data.get('owner_id')
        user = self.user_repo.get(owner_id)
        if not user:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data['title'],
            owner_id=owner_id,
            description=place_data.get('description', ''),
            price_per_night=place_data.get('price_per_night', 0)
        )
        self.place_repo.add(place)
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    # ======================
    # Reviews
    # ======================
    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=review_data['text'],
            user_id=user_id,
            place_id=place_id,
            rating=review_data.get('rating', 0)
        )
        self.review_repo.add(review)
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    # ======================
    # Amenities
    # ======================
    def create_amenity(self, amenity_data):
        if 'name' not in amenity_data:
            raise ValueError("Amenity name is required")

        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        if 'name' in data:
            amenity.name = data['name']

        return amenity


facade = HBnBFacade()

