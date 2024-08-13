from flask_restx import Namespace, Resource, fields

from employee_server.db import get_db

api = Namespace("employee_types", description="Employee types")


def get_api():
    """
    Returns types API.
    """
    return api


employee_type = api.model(
    "EmployeeType",
    {
        "id": fields.Integer(required=True, description="Type id"),
        "name": fields.String(required=True, description="Type name"),
    },
)


@api.route("/")
class EmployeeType(Resource):
    @api.doc("get_employee_types")
    @api.marshal_list_with(employee_type)
    def get(self):
        """
        Returns list of supported employee types.
        """
        db = get_db()
        employee_types = db.execute(
            "SELECT id, name FROM employee_types"
        ).fetchall()
        return employee_types
