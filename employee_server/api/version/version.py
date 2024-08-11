from flask_restx import Resource, Namespace, fields

api = Namespace("version", description="Version information")


version_info = {"version": "X.X.X"}


def get_api():
    """
    Returns version API.
    """
    return api


def set_version(ver: str):
    """
    Sets the version of the API.

    :param str ver:
        The version to set.

    """
    version_info["version"] = ver


version = api.model(
    "Version",
    {"version": fields.String(required=True, description="Current version")},
)


@api.route("/")
class Version(Resource):
    @api.doc("get_version")
    @api.marshal_with(version)
    def get(self):
        """
        Returns current version information.
        """
        return {"version": version_info["version"]}
