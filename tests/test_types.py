import json


def test_types(client):
    response = client.get("/types", follow_redirects=True)
    types = json.loads(response.data)
    assert types == {1: "Full time", 2: "Part time", 3: "Contractor"}
