from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.review import Review


class ReviewRepository(SQLAlchemyRepository):
    def init(self):
        super().init(Review)

    def get_by_user_and_place(self, user_id, place_id):
        return Review.query.filter_by(user_id=user_id, place_id=place_id).first()
