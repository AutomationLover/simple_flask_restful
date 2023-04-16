import pytest
from src.simple_flask_restful.reqparse import get_args_from_request
from flask import Flask

app = Flask(__name__)


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_args_from_request(client):
    # Test when request is JSON
    json_data = {'name': 'John', 'age': 25, 'gender': 'male'}
    # The line response = client.post('/', json=json_data) is used to simulate a POST request
    # to the root URL / of the Flask application, passing in the json_data dictionary as the request body.
    response = client.post('/', json=json_data)
    with app.test_request_context('/', json=json_data):
        args = get_args_from_request()
        assert args == json_data
    
    # Test when request is not JSON
    query_string = 'name=Jane&age=30&gender=female'
    response = client.get('/?' + query_string)
    with app.test_request_context('/?' + query_string):
        args = get_args_from_request()
        expected_args = {'name': 'Jane', 'age': '30', 'gender': 'female'}
        assert args == expected_args
