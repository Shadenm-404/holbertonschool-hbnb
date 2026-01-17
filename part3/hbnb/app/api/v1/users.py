from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace("users", description="User operations")

# ======================
# API Models
# ======================

user_model = api.model("User", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
    "first_name": fields.String(description="First name"),
    "last_name": fields.String(description="Last name"),
})

update_user_model = api.model("UpdateUser", {
    "first_name": fields.String(description="First name"),
    "last_name": fields.String(description="Last name"),
})

user_response_model = api.model("UserResponse", {
    "id": fields.String,
    "email": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "is_admin": fields.Boolean,
})

# ======================
# Routes
# ======================

@api.route("/")
class Users(Resource):

    @api.expect(user_model)
    @api.marshal_with(user_response_model, code=201)
    def post(self):
        """Create a new user (password is hashed)"""
        data = api.payload

        user = facade.create_user(
            email=data["email"],
            password=data["password"],
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
        )

        return user, 201

    @api.marshal_list_with(user_response_model)
    def get(self):
        """Get all users"""
        users = facade.user_repo.get_all()
        return users, 200


@api.route("/<string:user_id>")
class User(Resource):

    @api.marshal_with(user_response_model)
    def get(self, user_id):
        """Get user by ID"""
        user = facade.user_repo.get_by_id(user_id)
        if not user:
            api.abort(404, "User not found")
        return user, 200

    @api.expect(update_user_model)
    @api.marshal_with(user_response_model)
    @jwt_required()
    def put(self, user_id):
        """Update user (owner only)"""
        current_user_id = get_jwt_identity()

        # المستخدم يعدّل نفسه فقط
        if current_user_id != user_id:
            api.abort(403, "You can only update your own profile")

        user = facade.user_repo.get_by_id(user_id)
        if not user:
            api.abort(404, "User not found")

        data = api.payload

        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        facade.user_repo.update()
        return user, 200

