from flask_restx import Api

from .version import api as ns1

api = Api(
    title="Employee registry", version="0.0.1", description="Employee registry API"
)

api.add_namespace(ns1, "/version")
