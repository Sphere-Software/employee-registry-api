import json


def test_types(client):
    response = client.get("/types", follow_redirects=True)
    expected = [
        {"id": 1, "name": "Full time"},
        {"id": 2, "name": "Part time"},
        {"id": 3, "name": "Contractor"},
    ]

    types = json.loads(response.data)
    assert types == expected
