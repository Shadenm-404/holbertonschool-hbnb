class Config:
    SECRET_KEY = "super-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"


config = {
    "development": DevelopmentConfig,
}
