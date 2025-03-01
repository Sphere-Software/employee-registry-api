from flask_restx import Api
from importlib import metadata

from .version import version as ns1
from .employee_types import employee_type as ns2
from .teams import team as ns3

import flask


def setup_api(app: flask.Flask):
    """
    Initializes RESTX with given Flask application.

    :param flask.Flask app: A Flask application.
    """
    md = metadata.metadata(__package__.split(".")[0])
    name = md["name"]
    ver = md["version"]
    desc = md["summary"]
    api = Api(
        title=name,
        version=ver,
        description=desc,
    )

    ns1.set_version(ver)
    api.add_namespace(ns1.get_api(), "/version")
    api.add_namespace(ns2.get_api(), "/employee_types")
    api.add_namespace(ns3.get_api(), "/teams")
    api.init_app(app)
