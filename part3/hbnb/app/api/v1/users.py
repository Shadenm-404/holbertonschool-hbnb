from flask_restx import Resource, Namespace, fields
from app.services.facade import facade

api = Namespace('users', description='User operations')

# ======================
# Models
# ======================

user_model = api.model('User', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

# ======================
# Routes
# ======================

@api.route('/')
class Users(Resource):

    @api.expect(user_model)
    def post(self):
        """Create a new user"""
        try:
            user = facade.create_user(api.payload)
            return user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200


@api.route('/<string:user_id>')
class User(Resource):

    def get(self, user_id):
        """Get user by ID"""
        user = facade.user_repo.get(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict(), 200

    @api.expect(update_user_model)
    def put(self, user_id):
        """Update user"""
        user = facade.user_repo.get(user_id)
        if not user:
            api.abort(404, "User not found")

        data = api.payload

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']

        return user.to_dict(), 200

