import unittest
from unittest.mock import patch, MagicMock
from src.simple_flask_restful.decorator_method import decorator_method, BadRequest, CustomException


class TestRestfulMethod(unittest.TestCase):

    def test_bad_request(self):
        @decorator_method
        def test():
            raise BadRequest("Bad Request")

        with patch('src.simple_flask_restful.decorator_method.jsonify', MagicMock()) as mock_jsonify:
            response = test()
            mock_jsonify.assert_called_once_with({"message": "Bad Request"})
            self.assertEqual(response[0], mock_jsonify.return_value)
            self.assertEqual(response[1], 400)

    def test_custom_exception(self):
        @decorator_method
        def test():
            raise CustomException(403, "Forbidden")

        with patch('src.simple_flask_restful.decorator_method.jsonify', MagicMock()) as mock_jsonify:
            response = test()
            mock_jsonify.assert_called_once_with({"message": "Forbidden"})
            self.assertEqual(response[0], mock_jsonify.return_value)
            self.assertEqual(response[1], 403)

    def test_successful_request(self):
        @decorator_method
        def test():
            return {"data": "Hello World"}, 200

        with patch('src.simple_flask_restful.decorator_method.jsonify', MagicMock()) as mock_jsonify:
            response = test()
            mock_jsonify.assert_not_called()
            self.assertEqual(response[0], {"data": "Hello World"})
            self.assertEqual(response[1], 200)

    def test_unhandled_exception(self):
        @decorator_method
        def test():
            raise Exception("Unhandled Exception")

        with self.assertRaises(Exception):
            test()
