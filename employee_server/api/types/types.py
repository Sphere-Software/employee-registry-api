from flask_restx import Resource, Namespace, fields
from flask import current_app as app

api = Namespace("types", description="Employee types")


def get_api():
    """
    Returns types API.
    """
    return api


types = api.model(
    "Types",
    {
        "id": fields.Integer(required=True, description="Type id"),
        "name": fields.String(required=True, description="Type name"),
    },
)


@api.route("/")
class Type(Resource):
    @api.doc("get")
    @api.marshal_list_with(types)
    def get(self):
        """
        Returns list of supported employee types.
        """
        app.logger.warning("FAK!")
        return [{"id": 1, "name": "Full time"}]
