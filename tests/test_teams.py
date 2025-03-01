import json

import pytest
from flask_restx._http import HTTPStatus

from employee_server import create_app
from employee_server.db import get_db, init_db
from employee_server.models.team import Team


@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test.
    """
    # Create a temporary file to isolate the database for each test.
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})

    # Create the database and load test data
    with app.app_context():
        init_db(app)
        teams = [Team("Foo team"), Team("Bar team")]
        session = get_db().session
        session.add_all(teams)
        session.commit()

    yield app


def test_get_all_teams(client):
    response = client.get("/teams", follow_redirects=True)
    expected = [
        {"id": 1, "name": "Foo team"},
        {"id": 2, "name": "Bar team"},
    ]
    teams = json.loads(response.data)
    assert teams == expected
    assert response.status_code == HTTPStatus.OK.value


def test_get_team(client):
    response = client.get("/teams/2", follow_redirects=True)
    expected = {"id": 2, "name": "Bar team"}
    team = json.loads(response.data)
    assert team == expected
    assert response.status_code == HTTPStatus.OK.value


def test_new_team(client):
    new_team = {"name": "Baz team"}
    response = client.post("/teams", json=new_team, follow_redirects=True)
    json_data = json.loads(response.data)
    assert json_data["id"] != 0
    assert json_data["name"] == new_team["name"]
    assert response.status_code == HTTPStatus.CREATED.value


def test_new_team_duplicate_name(client):
    new_team = {"name": "Baz team"}
    client.post("/teams", json=new_team, follow_redirects=True)
    response = client.post("/teams", json=new_team, follow_redirects=True)
    assert response.status_code == HTTPStatus.CONFLICT.value


def test_team_does_not_exist(client):
    response = client.get("/teams/42", follow_redirects=True)
    assert response.status_code == HTTPStatus.NOT_FOUND.value
