import pytest
from unittest.mock import patch
from src.simple_flask_restful.reqparse import RequestParser, BadRequest


@pytest.fixture
def client():
    from flask import Flask, jsonify, request

    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            return jsonify({'message': 'Hello, world!'})
        elif request.method == 'POST':
            return jsonify(request.json)
        else:
            return jsonify({'error': 'Method not allowed'}), 405

    with app.test_client() as client:
        yield client


@pytest.fixture
def parser():
    parser = RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('age', type=int, default=18)
    parser.add_argument('gender', choices=['male', 'female'], default='male')
    return parser


@pytest.mark.parametrize("test_input, expected_output, strict, bundle_errors", [
    # Test 1: Required argument is missing
    ({'age': '25', 'gender': 'male'},
     {'message': "name is required."},
     True, False),
    # Test 2: Valid request with all arguments provided
    ({'name': 'John Doe', 'age': '25', 'gender': 'male'},
     {'name': 'John Doe', 'age': 25, 'gender': 'male'},
     True, False),
    # Test 3: Valid request with default argument values
    ({'name': 'John Doe'}, {'name': 'John Doe', 'age': 18, 'gender': 'male'},
     False, False),
    # Test 4: Invalid argument value provided
    ({'name': 'John Doe', 'age': 'invalid', 'gender': 'male'},
     {'message': "age should be int."},
     True, False),
    # Test 5: Invalid choice for argument value provided
    ({'name': 'John Doe', 'age': '25', 'gender': 'invalid'},
     {'message': "gender must be one of ['male', 'female']."},
     True, False),
    # Test 6: Bundle errors with multiple errors
    ({'age': 'invalid', 'gender': 'invalid'},
     {'age': 'age should be int.', 'gender': "gender must be one of ['male', 'female'].",  'name': 'name is required.'},
     True, True),
    # Test 7: Bundle errors with single error
    ({'name': 'Luke', 'age': '25', 'gender': 'invalid'},
     {'gender': "gender must be one of ['male', 'female']."},
      True, True),
])
def test_request_parser(client, parser, test_input, expected_output, strict, bundle_errors):
    with patch('src.simple_flask_restful.reqparse.get_args_from_request', return_value=test_input):
        if bundle_errors:
            with pytest.raises(BadRequest) as excinfo:
                parser.parse_args(strict=strict, bundle_errors=bundle_errors)
            assert excinfo.value.args[0] == expected_output
        else:
            if expected_output.get('message'):
                with pytest.raises(BadRequest) as excinfo:
                    parser.parse_args(strict=strict)
                assert str(excinfo.value) == expected_output['message']
            else:
                output = parser.parse_args(strict=strict)
                assert output == expected_output



