import json


def test_get_all_teams(client):
    response = client.get("/teams", follow_redirects=True)
    expected = [
        {"id": 1, "name": "Foo team"},
        {"id": 2, "name": "Bar team"},
    ]
    teams = json.loads(response.data)
    assert teams == expected


def test_get_team(client):
    response = client.get("/teams/2", follow_redirects=True)
    expected = {"id": 2, "name": "Bar team"}
    team = json.loads(response.data)
    assert team == expected


def test_new_team(client):
    new_team = {"name": "Baz team"}
    response = client.post("/teams", json=new_team, follow_redirects=True)
    json_data = json.loads(response.data)
    assert json_data["id"] != 0
    assert json_data["name"] == new_team["name"]


def test_new_team_duplicate_name(client):
    new_team = {"name": "Baz team"}
    client.post("/teams", json=new_team, follow_redirects=True)
    response = client.post("/teams", json=new_team, follow_redirects=True)
    assert response.status_code == 400


def test_team_does_not_exist(client):
    response = client.get("/teams/42", follow_redirects=True)
    assert response.status_code == 404
