import pytest

from src.simple_flask_restful.reqparse import Parser, BadRequest


@pytest.fixture
def parser():
    parser = Parser()
    parser.add_argument('name', required=True)
    parser.add_argument('age', type=int)
    parser.add_argument('gender', choices=['male', 'female'])
    return parser


@pytest.mark.parametrize('request_args, strict, bundle_errors, expected_args, expect_error', [
    ({'name': 'John'}, True, False, {'name': 'John', 'age': None, 'gender': None}, None),
    ({'name': 'John', 'age': '25'}, True, False, {'name': 'John', 'age': 25, 'gender': None}, None),
    ({'name': 'John', 'age': 'not_a_number'}, True, True, None, {'age': 'age should be int.'}),
    ({'name': 'John', 'gender': 'unknown'}, True, True, None, {'gender': 'gender must be one of [\'male\', \'female\'].'}),
    ({'age': '25'}, True, True, None, {'name': 'name is required.'}),
    ({'name': 'John', 'age': 'not_a_number'}, True, False, None, 'age should be int.'),
    ({'name': 'John', 'gender': 'unknown'}, True, False, None, 'gender must be one of [\'male\', \'female\'].'),
    ({'age': '25'}, True, False, None, 'name is required.')
])
def test_parser_parse_args(parser, request_args, strict, bundle_errors, expected_args, expect_error):
    if expect_error:
        with pytest.raises(BadRequest) as excinfo:
            parser.parse_args(request_args, strict, bundle_errors)
        if bundle_errors:
            assert excinfo.value.args[0] == expect_error
        else:
            assert expect_error in str(excinfo.value)
    else:
        args = parser.parse_args(request_args, strict, bundle_errors)
        assert args == expected_args
