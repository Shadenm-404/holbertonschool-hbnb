from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # --- User methods ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # allow only specific fields
        allowed = {"first_name", "last_name", "email"}
        updates = {k: v for k, v in user_data.items() if k in allowed}

        # email uniqueness check
        if "email" in updates:
            existing = self.get_user_by_email(updates["email"])
            if existing and existing.id != user_id:
                raise ValueError("Email already registered")

        for key, value in updates.items():
            setattr(user, key, value)

        self.user_repo.update(user_id, user)
        return user

# ---------- Amenity methods ----------
def create_amenity(self, amenity_data):
    amenity = Amenity(**amenity_data)
    self.amenity_repo.add(amenity)
    return amenity

def get_amenity(self, amenity_id):
    return self.amenity_repo.get(amenity_id)

def get_all_amenities(self):
    return self.amenity_repo.get_all()

def update_amenity(self, amenity_id, amenity_data):
    amenity = self.amenity_repo.get(amenity_id)
    if not amenity:
        return None

    allowed = {"name"}
    updates = {k: v for k, v in amenity_data.items() if k in allowed}

    amenity.update(updates)
    return amenity

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
