from flask_restx import Resource, Namespace, fields

api = Namespace("version", description="Version information")

version = api.model(
    "Version",
    {"version": fields.String(required=True, description="Current version")},
)


@api.route("/")
class Version(Resource):
    @api.doc("get")
    @api.marshal_with(version)
    def get(self):
        """Returns current version information"""
        return {"version": "0.0.1"}
