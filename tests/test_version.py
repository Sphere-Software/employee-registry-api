import json


def test_version(client):
    response = client.get("/version", follow_redirects=True)
    version_info = json.loads(response.data)
    assert version_info["version"] == "0.1.0"
