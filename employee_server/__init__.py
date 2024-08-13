import os

from flask import Flask

from .api import setup_api


def create_app(test_config=None):
    """
    Create and configure an instance of the flask application.

    :param test_config: Configuration for testing.
    """
    app = Flask(__name__, instance_relative_config=True)
    database_uri = os.path.join(app.instance_path, "employee-server.sqlite")
    app.logger.debug(f"Database uri: {database_uri}")
    app.config.from_mapping(
        # A default secret key that should be overridden by instance config.
        SECRET_KEY="dev",
        # Store the databae in the instance folder.
        SQLALCHEMY_DATABASE_URI=f"sqlite://{database_uri}",
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in.
        app.config.update(test_config)

    # Ensure that the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register the database commands.
    from . import db

    db.init_app(app)
    setup_api(app)

    return app
