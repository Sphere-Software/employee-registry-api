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
