import json
import toml


def test_version(client):
    with open("pyproject.toml", "r") as f:
        expected = toml.load(f)
    response = client.get("/version", follow_redirects=True)
    version_info = json.loads(response.data)
    assert version_info["version"] == expected["project"]["version"]
