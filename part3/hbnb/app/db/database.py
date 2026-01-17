from sqlalchemy import create_engine
from config import config


def get_engine(env="development"):
    return create_engine(
        config[env].SQLALCHEMY_DATABASE_URI,
        echo=False,
        future=True
    )
