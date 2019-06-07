import pytest
import run_server
import json


@pytest.fixture
def client():
    client = run_server.app.test_client()
    yield client


class TestServer:
    def test_hello_response(self, client):
        response = client.get(
            '/hello')
        r_data = json.loads(response.get_data())
        assert r_data['message'] == 'server running'
        assert r_data['Content-Type'] == 'application/json'
