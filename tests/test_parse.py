import pytest

from src.simple_flask_restful.reqparse import Parser, BadRequest


@pytest.fixture
def parser():
    parser = Parser()
    parser.add_argument('name', required=True)
    parser.add_argument('age', type=int)
    parser.add_argument('gender', choices=['male', 'female'])
    return parser


@pytest.mark.parametrize('request_args, strict, expected_args, expect_error', [
    ({'name': 'John'}, True, {'name': 'John', 'age': None, 'gender': None}, None),
    ({'name': 'John', 'age': '25'}, True, {'name': 'John', 'age': 25, 'gender': None}, None),
    ({'name': 'John', 'age': 'not_a_number'}, True, None, 'age should be int.'),
    ({'name': 'John', 'gender': 'unknown'}, True, None, 'gender must be one of [\'male\', \'female\'].'),
    ({'age': '25'}, True, None, 'name is required.')
])
def test_parser_parse_args(parser, request_args, strict, expected_args, expect_error):
    if expect_error:
        with pytest.raises(BadRequest) as excinfo:
            parser.parse_args(request_args, strict)
        assert expect_error in str(excinfo.value)
    else:
        args = parser.parse_args(request_args, strict)
        assert args == expected_args


