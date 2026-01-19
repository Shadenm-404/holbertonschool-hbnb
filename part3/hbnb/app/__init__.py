from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager

from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns
#from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns

jwt = JWTManager()

def create_app(config_class):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Init JWT
    jwt.init_app(app)

    # Init API
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/"
    )

    # Register namespaces
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    #api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")

    return app
