from flask_restx import Resource, Namespace, fields
from enum import Enum, unique

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


employee_types = [
    {"id": 1, "name": "Full time"},
    {"id": 2, "name": "Part time"},
    {"id": 3, "name": "Contractor"},
]


@api.route("/")
class Type(Resource):
    @api.doc("get")
    @api.marshal_list_with(types)
    def get(self):
        """
        Returns list of supported employee types.
        """

        return employee_types
