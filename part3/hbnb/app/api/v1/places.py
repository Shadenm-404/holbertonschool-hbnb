from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace("places", description="Place operations")

place_create_model = api.model("PlaceCreate", {
    "title": fields.String(required=True, description="Place title"),
    "description": fields.String(description="Place description"),
    "price_per_night": fields.Float(description="Price per night")
})

place_update_model = api.model("PlaceUpdate", {
    "title": fields.String(description="Place title"),
    "description": fields.String(description="Place description"),
    "price_per_night": fields.Float(description="Price per night")
})


@api.route("/")
class Places(Resource):
    def get(self):
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

    @api.expect(place_create_model, validate=True)
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()

        payload = api.payload or {}
        payload["owner_id"] = current_user_id  # enforce owner from token

        try:
            place = facade.create_place(payload)
            return place.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route("/<string:place_id>")
class PlaceResource(Resource):
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return place.to_dict(), 200

    @api.expect(place_update_model, validate=True)
    @jwt_required()
    def put(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        current_user_id = get_jwt_identity()

        if not is_admin and place.owner_id != current_user_id:
            api.abort(403, "Forbidden")

        data = api.payload or {}

        if "title" in data and data["title"] is not None:
            place.title = data["title"]
        if "description" in data and data["description"] is not None:
            place.description = data["description"]
        if "price_per_night" in data and data["price_per_night"] is not None:
            place.price_per_night = data["price_per_night"]

        facade.place_repo.update()
        return place.to_dict(), 200

    @jwt_required()
    def delete(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        current_user_id = get_jwt_identity()

        if not is_admin and place.owner_id != current_user_id:
            api.abort(403, "Forbidden")

        facade.place_repo.delete(place)
        return {"message": "Place deleted"}, 200
