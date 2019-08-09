import pytest
import run_server
import json
import yaml

with open('yamls/secret_server_setting.yml', 'r') as yf:
    server_settings = yaml.load(yf)


@pytest.fixture
def client():
    client = run_server.app.test_client()
    yield client


class TestServer:
    def test_hello_response(self, client):
        response = client.get('/hello')
        r_data = json.loads(response.get_data())
        assert r_data['message'] == 'server running'
        assert r_data['Content-Type'] == 'application/json'

    def test_incoming(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {
            'key': server_settings['key'],
            'text': '日本語もじじ'
        }
        url = '/incoming'

        response = client.post(url, data=json.dumps(data), headers=headers)
        assert response.status_code == 200

        r_data = json.loads(response.get_data())

        assert r_data['message'] == 'using valid key'
        assert r_data['text'] == '日本語もじじ'
