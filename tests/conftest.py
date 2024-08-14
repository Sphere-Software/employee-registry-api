import pytest

from employee_server import create_app
from employee_server.db import init_db


@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test.
    """
    # Create an in memory database to isolate it for for each test.
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})

    # Create the database tables
    with app.app_context():
        init_db(app)

    yield app


@pytest.fixture
def client(app):
    """
    A test client for the app.
    """
    return app.test_client()
