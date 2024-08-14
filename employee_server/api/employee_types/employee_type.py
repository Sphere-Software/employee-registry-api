from flask_restx import Namespace, Resource, fields

from employee_server.models.employee_type import EmployeeType as TypeModel

api = Namespace("employee_types", description="Employee types")


def get_api():
    """
    Returns types API.
    """
    return api


employee_type_model = api.model(
    "EmployeeType",
    {
        "id": fields.Integer(required=True, description="Type id"),
        "name": fields.String(required=True, description="Type name"),
    },
)


@api.route("/")
class EmployeeType(Resource):
    @api.doc("get_employee_types")
    @api.marshal_list_with(employee_type_model)
    def get(self):
        """
        Returns list of supported employee types.
        """
        employee_types = TypeModel.query.all()
        return employee_types
