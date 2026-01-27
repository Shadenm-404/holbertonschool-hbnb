from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.user import User


class UserRepository(SQLAlchemyRepository):
    def __init__(self, session):
        super().__init__(session, User)

    def get_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()
