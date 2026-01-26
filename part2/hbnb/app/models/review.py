from app.models.base_model import BaseModel
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        self._validate_text(text)
        self._validate_rating(rating)
        self._validate_user(user)
        self._validate_place(place)

        self.text = text.strip()
        self.rating = rating
        self.place = place
        self.user = user

    def _validate_text(self, text):
        if not isinstance(text, str):
            raise TypeError("text must be a string.")
        if not text.strip():
            raise ValueError("Review text is required.")

    def _validate_rating(self, rating):
        if not isinstance(rating, int):
            raise TypeError("rating must be an integer.")
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5.")

    def _validate_user(self, user):
        if not isinstance(user, User):
            raise TypeError("user must be a User instance.")

    def _validate_place(self, place):
        from app.models.place import Place
        if not isinstance(place, Place):
            raise TypeError("place must be a Place instance.")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user": self.user.id,
            "place": self.place.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
