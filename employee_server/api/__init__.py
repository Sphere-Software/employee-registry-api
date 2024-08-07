from flask_restx import Api
from importlib import metadata

from .version import version as ns1

import flask
import toml


def setup_api(app: flask.Flask):
    """
    Initializes RESTX with given Flask application.

    :param flask.Flask app: A Flask application.
    """
    try:
        md = metadata.metadata(__package__.split(".")[0])
        name = md["name"]
        ver = md["version"]
        desc = md["summary"]
    except metadata.PackageNotFoundError:
        app.logger.warning(
            "Running from the source code! DO NOT USE THIS IN PRODUCTION!"
        )
        with open("./pyproject.toml", "r") as f:
            md = toml.load(f)
        name = md["project"]["name"]
        ver = md["project"]["version"]
        desc = md["project"]["description"]

    api = Api(
        title=name,
        version=ver,
        description=desc,
    )

    api.add_namespace(ns1.get_api(), "/version")
    api.init_app(app)
