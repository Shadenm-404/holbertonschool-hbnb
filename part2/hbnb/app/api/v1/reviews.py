from flask_restx import Resource, Namespace, fields
from app.services.facade import facade

api = Namespace('reviews', description='Review operations')


review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User id'),
    'place_id': fields.String(required=True, description='Place id'),
})

update_review_model = api.model('UpdateReview', {
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
})


def _review_dict(review):
    data = review.to_dict() if hasattr(review, "to_dict") else {}
    
    return data


@api.route('/')
class Reviews(Resource):

    @api.expect(review_model)
    def post(self):
        """Create a new review"""
        try:
            review = facade.create_review(api.payload)
            return _review_dict(review), 201
        except (TypeError, ValueError) as e:
            api.abort(400, str(e))

    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [_review_dict(r) for r in reviews], 200


@api.route('/<string:review_id>')
class ReviewResource(Resource):

    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return _review_dict(review), 200

    @api.expect(update_review_model)
    def put(self, review_id):
        """Update review"""
        data = api.payload or {}
        try:
            review = facade.update_review(review_id, data)
            if not review:
                api.abort(404, "Review not found")
            return _review_dict(review), 200
        except (TypeError, ValueError) as e:
            api.abort(400, str(e))

    def delete(self, review_id):
        """Delete review"""
        review = facade.delete_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return {"message": "Review deleted"}, 200
