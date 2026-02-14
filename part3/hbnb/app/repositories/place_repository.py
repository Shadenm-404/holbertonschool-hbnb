from app.extensions import db
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.place import Place


class PlaceRepository(SQLAlchemyRepository):
    def init(self):
        super().init(Place)

    def get_by_owner(self, user_id):
        return self.model.query.filter_by(owner_id=user_id).all()
