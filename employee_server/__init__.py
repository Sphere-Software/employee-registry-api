import os

from flask import Flask

from .api import setup_api


def create_app(test_config=None):
    """
    Create and configure an instance of the flask application.

    :param test_config: Configuration for testing.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # A default secret key that should be overridden by instance config.
        SECRET_KEY="dev",
        # Store the databae in the instance folder.
        DATABASE=os.path.join(app.instance_path, "employee-server.sqlite"),
    )
    setup_api(app)

    return app
