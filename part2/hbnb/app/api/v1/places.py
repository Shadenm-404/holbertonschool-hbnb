from flask_restx import Resource, Namespace, fields
from app.services.facade import facade

api = Namespace('places', description='Place operations')

# ======================
# Models (Swagger)
# ======================

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner (User) id'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

update_place_model = api.model('UpdatePlace', {
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

# ======================
# Helpers
# ======================

def _user_public_dict(user):
    data = user.to_dict() if hasattr(user, "to_dict") else {}
    data.pop("password", None)
    return data


def _place_basic(place):
    return {
        "id": place.id,
        "title": place.title,
        "latitude": place.latitude,
        "longitude": place.longitude,
    }


def _place_full(place):
    owner_obj = getattr(place, "owner", None)
    owner_dict = _user_public_dict(owner_obj) if owner_obj else None
    owner_id = owner_obj.id if owner_obj else None

    amenities = getattr(place, "amenities", []) or []
    amenities_list = []
    amenity_ids = []

    for a in amenities:
        amenity_ids.append(a.id)
        amenities_list.append(
            a.to_dict() if hasattr(a, "to_dict") else {"id": a.id}
        )

    return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,

        # owner
        "owner_id": owner_id,
        "owner": owner_dict,

        # amenities
        "amenities": amenities_list,   # nested details (المطلوب)
        "amenity_ids": amenity_ids,    # IDs (احتياط للاختبارات)

        "created_at": place.created_at.isoformat() if hasattr(place, "created_at") else None,
        "updated_at": place.updated_at.isoformat() if hasattr(place, "updated_at") else None,
    }

# ======================
# Routes
# ======================

@api.route('/')
class Places(Resource):

    @api.expect(place_model)
    def post(self):
        """Create a new place"""
        try:
            place = facade.create_place(api.payload)
            return _place_full(place), 201
        except (TypeError, ValueError) as e:
            api.abort(400, str(e))

    def get(self):
        """Get all places (basic details)"""
        places = facade.get_all_places()
        return [_place_basic(p) for p in places], 200


@api.route('/<string:place_id>')
class Place(Resource):

    def get(self, place_id):
        """Get place by ID (full details)"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return _place_full(place), 200

    @api.expect(update_place_model)
    def put(self, place_id):
        """Update place"""
        data = api.payload or {}
        try:
            place = facade.update_place(place_id, data)
            if not place:
                api.abort(404, "Place not found")
            return _place_full(place), 200
        except (TypeError, ValueError) as e:
            api.abort(400, str(e))
