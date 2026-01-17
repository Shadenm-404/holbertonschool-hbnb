from sqlalchemy.orm import sessionmaker
from app.db.database import get_engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_engine()
)
