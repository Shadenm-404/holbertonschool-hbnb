from app.persistence.repository import Repository, InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo: Repository = InMemoryRepository()
        self.place_repo: Repository = InMemoryRepository()
        self.review_repo: Repository = InMemoryRepository()
        self.amenity_repo: Repository = InMemoryRepository()

    # ======================
    # Users
    # ======================
    
    def create_user(self, user_data):
        if not isinstance(user_data, dict):
            raise TypeError("user_data must be a dictionary.")

        email = user_data.get("email")
        if email is None:
            raise ValueError("Email is required")

        existing_users = self.user_repo.get_all()
        for user in existing_users:
            if user.email == email:
                raise ValueError("User with this email already exists")

        first_name = user_data.get("first_name", "")
        last_name = user_data.get("last_name", "")

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_admin=user_data.get("is_admin", False)
        )

        self.user_repo.add(user)
        return user


    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        if not isinstance(user_data, dict):
            raise TypeError("user_data must be a dictionary.")

        if "first_name" in user_data:
            first_name = user_data["first_name"]
            if not isinstance(first_name, str):
                raise TypeError("first_name must be a string.")
            first_name = first_name.strip()
            if not first_name:
                raise ValueError("first_name is required.")
            if len(first_name) > 50:
                raise ValueError("first_name must be at most 50 characters.")
            user.first_name = first_name

        if "last_name" in user_data:
            last_name = user_data["last_name"]
            if not isinstance(last_name, str):
                raise TypeError("last_name must be a string.")
            last_name = last_name.strip()
            if not last_name:
                raise ValueError("last_name is required.")
            if len(last_name) > 50:
                raise ValueError("last_name must be at most 50 characters.")
            user.last_name = last_name

        user.save()
        return user

    # ======================
    # Places
    # ======================
    def create_place(self, place_data):
        if not isinstance(place_data, dict):
            raise TypeError("place_data must be a dictionary.")

        # required fields
        title = place_data.get("title")
        owner_id = place_data.get("owner_id")

        if owner_id is None:
            raise ValueError("owner_id is required.")

        # get owner object
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        # optional fields
        description = place_data.get("description", "")
        price = place_data.get("price")
        latitude = place_data.get("latitude")
        longitude = place_data.get("longitude")
        amenity_ids = place_data.get("amenities", [])

        # validate amenities ids list
        if amenity_ids is None:
            amenity_ids = []
        if not isinstance(amenity_ids, list):
            raise TypeError("amenities must be a list of amenity ids.")

        # create place (Place model will validate title/price/lat/long/owner)
        place = Place(
            owner=owner,
            title=title,
            price=price,
            latitude=latitude,
            longitude=longitude,
            description=description
        )

        # attach amenities
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity not found: {amenity_id}")
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary.")

        # update allowed fields with validation (using Place setters / checks)
        if "title" in data:
            title = data["title"]
            if not isinstance(title, str):
                raise TypeError("title must be a string.")
            title = title.strip()
            if not title:
                raise ValueError("title is required.")
            if len(title) > 100:
                raise ValueError("title must be at most 100 characters.")
            place.title = title

        if "description" in data:
            desc = data["description"]
            if desc is None:
                desc = ""
            if not isinstance(desc, str):
                raise TypeError("description must be a string.")
            place.description = desc.strip()

        if "price" in data:
            place.price = data["price"]  # validated by setter

        if "latitude" in data:
            place.latitude = data["latitude"]  # validated by setter

        if "longitude" in data:
            place.longitude = data["longitude"]  # validated by setter

        # amenities update (optional): replace list if provided
        if "amenities" in data:
            amenity_ids = data["amenities"]
            if amenity_ids is None:
                amenity_ids = []
            if not isinstance(amenity_ids, list):
                raise TypeError("amenities must be a list of amenity ids.")

            new_amenities = []
            for amenity_id in amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity not found: {amenity_id}")
                new_amenities.append(amenity)

            place.amenities = []
            for a in new_amenities:
                place.add_amenity(a)

        place.save()
        return place

    # ======================
    # Reviews
    # ======================
    def create_review(self, review_data):
        if not isinstance(review_data, dict):
            raise TypeError("review_data must be a dictionary.")

        text = review_data.get("text")
        rating = review_data.get("rating")
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        if user_id is None:
            raise ValueError("user_id is required.")
        if place_id is None:
            raise ValueError("place_id is required.")

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        review = Review(text=text, rating=rating, place=place, user=user)

        self.review_repo.add(review)

        place.add_review(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None 
            
        return list(getattr(place, "reviews", []))

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary.")

        if "text" in data:
            text = data["text"]
            if not isinstance(text, str):
                raise TypeError("text must be a string.")
            text = text.strip()
            if not text:
                raise ValueError("text is required.")
            review.text = text

        if "rating" in data:
            rating = data["rating"]
            if not isinstance(rating, int):
                raise TypeError("rating must be an integer.")
            if rating < 1 or rating > 5:
                raise ValueError("rating must be between 1 and 5.")
            review.rating = rating

        review.save()
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        place = getattr(review, "place", None)
        if place and hasattr(place, "reviews"):
            try:
                place.reviews = [r for r in place.reviews if r.id != review.id]
                place.save()
            except Exception:
                pass

        self.review_repo.delete(review_id)
        return review

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

