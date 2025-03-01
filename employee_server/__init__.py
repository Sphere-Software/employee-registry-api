import os

from flask import Flask

from .api import setup_api
from .models.employee_type import EmployeeType


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
        SQLALCHEMY_DATABASE_URI="sqlite://",
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in.
        app.config.update(test_config)

    # TODO: Do we really need this?
    # Ensure that the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register the database commands.
    from . import db

    db.init_app(app)
    setup_api(app)

    with app.app_context():
        data = [
            EmployeeType(1, "Full time"),
            EmployeeType(2, "Part time"),
            EmployeeType(3, "Contractor"),
        ]
        session = db.get_db().session
        session.add_all(data)
        session.commit()

    return app
