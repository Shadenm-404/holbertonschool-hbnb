from app.extensions import db


class SQLAlchemyRepository:
    """
    Generic SQLAlchemy repository.
    Provides basic CRUD operations using Flask-SQLAlchemy.
    """

    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def get_by_id(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self):
        db.session.commit()

    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()
