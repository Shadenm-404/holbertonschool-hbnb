from app.extensions import db
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.review import Review


class ReviewRepository(SQLAlchemyRepository):
    def init(self):
        super().init(Review)

    def get_by_user_and_place(self, user_id, place_id):
        return (
            self.model.query
            .filter_by(user_id=user_id, place_id=place_id)
            .first()
        )
    def get_by_place_id(self, place_id):
        return Review.query.filter_by(place_id=place_id).order_by(Review.created_at.desc()).all()
