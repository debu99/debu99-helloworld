from flask import Flask
import json, os
from routes import configure_routes
import pytest

app = Flask(__name__)
configure_routes(app)
client = app.test_client()

def test_index_route():
    url = '/'

    response = client.get(url)
    assert response.status_code == 200
    assert b"Hello World from" in response.get_data()

def test_healthz_route():
    url = '/healthz'

    response = client.get(url)
    assert response.status_code == 200
    assert response.get_data() == b'200OK'

def test_hello_route_get():
    url = '/hello'

    response = client.get(url)
    assert response.status_code == 200
    assert response.get_data() == b'Please post data'

def test_hello_route_post():
    url = '/hello'

    mock_request_headers = {'Content-Type': 'application/json'}

    mock_request_data = {
        'request_id': '123',
        'payload': {
            'key1': 123,
            'key2': 'value2'
        }
    }
    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    correct_response_data = 'curl -i -XPOST -H "Content-Type: application/json" -d \'' + json.dumps(mock_request_data) + '\' http://localhost' + url + '\n\n' + json.dumps(mock_request_data)
    assert response.status_code == 200
    assert response.get_data().decode("utf-8") == correct_response_data

def test_post_route__success():
    url = '/post'

    mock_request_headers = {
        'authorization-sha256': '123'
    }

    mock_request_data = {
        'request_id': '123',
        'payload': {
            'py': 'pi',
            'java': 'script'
        }
    }

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 200


def test_post_route__failure__unauthorized():
    url = '/post'

    mock_request_headers = {}

    mock_request_data = {
        'request_id': '123',
        'payload': {
            'py': 'pi',
            'java': 'script'
        }
    }

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 401


def test_post_route__failure__bad_request():
    url = '/post'

    mock_request_headers = {
        'authorization-sha256': '123'
    }

    mock_request_data = {}

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 400


