from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


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

        for key, value in updates.items():
            setattr(amenity, key, value)

        self.amenity_repo.update(amenity_id, amenity)
        return amenity 
        
from app.models.place import Place


class HBnBFacade:

    # ---------- Place methods ----------

    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description"),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner=owner
        )

        for amenity_id in place_data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if "title" in place_data:
            title = place_data["title"]
            if not isinstance(title, str) or not title.strip():
                raise ValueError("title must be a non-empty string")
            if len(title.strip()) > 100:
                raise ValueError("title must be at most 100 characters")
            place.title = title.strip()

        if "description" in place_data:
            description = place_data["description"]
            if not isinstance(description, str):
                raise TypeError("description must be a string")
            place.description = description.strip()

        if "price" in place_data:
            price = place_data["price"]
            if not isinstance(price, (int, float)) or price < 0:
                raise ValueError("price must be a non-negative number")
            place.price = float(price)

        if "latitude" in place_data:
            latitude = place_data["latitude"]
            if not isinstance(latitude, (int, float)) or not -90 <= latitude <= 90:
                raise ValueError("latitude must be between -90 and 90")
            place.latitude = float(latitude)

        if "longitude" in place_data:
            longitude = place_data["longitude"]
            if not isinstance(longitude, (int, float)) or not -180 <= longitude <= 180:
                raise ValueError("longitude must be between -180 and 180")
            place.longitude = float(longitude)

        if "amenities" in place_data:
            place.amenities.clear()
            for amenity_id in place_data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

        place.save()
        return place
