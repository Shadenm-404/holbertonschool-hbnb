from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_access_token
from app.services.facade import facade

api = Namespace("auth", description="Authentication operations")

login_model = api.model("Login", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
})

token_model = api.model("Token", {
    "access_token": fields.String,
})


@api.route("/login")
class Login(Resource):

    @api.expect(login_model, validate=True)  
    @api.marshal_with(token_model)
    def post(self):
        data = api.payload or {}

        email = (data.get("email") or "").strip()
        password = data.get("password")

        if not email or not password:
            api.abort(400, "Missing email or password")

        user = facade.user_repo.get_by_email(email)
        if not user or not user.check_password(password):
            api.abort(401, "Invalid email or password")

        access_token = create_access_token(
            identity=user.id,
            additional_claims={"is_admin": user.is_admin}
        )

        return {"access_token": access_token}, 200
