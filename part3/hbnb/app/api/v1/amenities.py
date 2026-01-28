# app/api/v1/amenities.py

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import facade

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model("Amenity", {
    "name": fields.String(required=True, description="Name of the amenity")
})

update_amenity_model = api.model("AmenityUpdate", {
    "name": fields.String(description="Name of the amenity")
})


def require_admin():
    claims = get_jwt()
    if not claims.get("is_admin", False):
        api.abort(403, "Admin privileges required")


@api.route("/")
class AmenityList(Resource):
    def get(self):
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

    @api.expect(amenity_model, validate=True)
    @jwt_required()
    def post(self):
        require_admin()
        try:
            amenity = facade.create_amenity(api.payload or {})
            return amenity.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity.to_dict(), 200

    @api.expect(update_amenity_model, validate=True)
    @jwt_required()
    def put(self, amenity_id):
        require_admin()
        try:
            amenity = facade.update_amenity(amenity_id, api.payload or {})
            return amenity.to_dict(), 200
        except ValueError as e:
            # إذا "Amenity not found" -> 404 ، غيره غالبًا 400
            msg = str(e)
            if msg == "Amenity not found":
                api.abort(404, msg)
            api.abort(400, msg)
