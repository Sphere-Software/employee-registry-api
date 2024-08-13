import os
import tempfile

import pytest

from employee_server import create_app
from employee_server.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test.
    """

    # Create a temporary file to isolate the database for each test.
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # Create the database and load test data
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # Close and remote the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """
    A test client for the app.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    A test runner for the app's Click commands.
    """
    return app.test_cli_runner()
