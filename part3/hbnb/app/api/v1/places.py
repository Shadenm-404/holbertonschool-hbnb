from flask_restx import Resource, Namespace, fields
from app.services.facade import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'owner_id': fields.String(required=True, description='Owner ID'),
    'description': fields.String(description='Place description'),
    'price_per_night': fields.Float(description='Price per night')
})

@api.route('/')
class Places(Resource):
    @api.expect(place_model)
    def post(self):
        place = facade.create_place(api.payload)
        return place.to_dict(), 201

    def get(self):
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return place.to_dict(), 200

