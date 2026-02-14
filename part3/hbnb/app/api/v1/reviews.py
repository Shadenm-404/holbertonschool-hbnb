from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.facade import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    def get(self):
        try:
            place_id = request.args.get('place_id')

            if place_id:
                reviews = facade.get_reviews_by_place(place_id)
            else:
                reviews = facade.get_all_reviews()

            return [r.to_dict() for r in reviews], 200

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Error: {str(e)}")

    @api.expect(review_model)
    @jwt_required()
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            review_data = api.payload or {}

            rating = review_data.get('rating')
            try:
                rating_int = int(rating)
            except (TypeError, ValueError):
                api.abort(400, 'Rating must be between 1 and 5')

            if rating_int < 1 or rating_int > 5:
                api.abort(400, 'Rating must be between 1 and 5')

            review_data["user_id"] = current_user_id

            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Error: {str(e)}")
