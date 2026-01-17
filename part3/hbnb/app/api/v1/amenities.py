from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

update_amenity_model = api.model('AmenityUpdate', {
    'name': fields.String(description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    def post(self):
        amenity = facade.create_amenity(api.payload)
        return amenity.to_dict(), 201

    def get(self):
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')
        return amenity.to_dict(), 200

    @api.expect(update_amenity_model, validate=True)
    def put(self, amenity_id):
        amenity = facade.update_amenity(amenity_id, api.payload)
        if not amenity:
            api.abort(404, 'Amenity not found')
        return amenity.to_dict(), 200

