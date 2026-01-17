class SQLAlchemyRepository:
    """
    Generic SQLAlchemy repository.
    This class provides basic CRUD operations.
    """

    def __init__(self, session, model):
        self.session = session
        self.model = model

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_by_id(self, obj_id):
        return self.session.get(self.model, obj_id)

    def get_all(self):
        return self.session.query(self.model).all()

    def update(self):
        self.session.commit()

    def delete(self, obj):
        self.session.delete(obj)
        self.session.commit()
