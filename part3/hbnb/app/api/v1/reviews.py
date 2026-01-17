from flask_restx import Resource, Namespace, fields
from app.services.facade import facade  # ✅ نفس facade المشترك

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID'),
    'rating': fields.Integer(description='Rating (1-5)')
})

@api.route('/')
class Reviews(Resource):
    @api.expect(review_model)
    def post(self):
        """Create a new review"""
        try:
            review = facade.create_review(api.payload)
            return review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))
    
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews]
