import pytest
from flask import Flask
from src.simple_flask_restful import Api, Resource
from src.simple_flask_restful import abort


@pytest.fixture
def app():
    app = Flask(__name__)
    return app


class TestApi:
    
    def test_add_resource(self, app):
        api = Api(app)
        
        class TestResource(Resource):
            def get(self):
                return 'test'
        
        api.add_resource(TestResource, '/test')
        
        with app.test_client() as c:
            response = c.get('/test')
            assert response.status_code == 200
            assert response.data == b'"test"\n'
    
    def test_add_post_resource(self, app):
        api = Api(app)
        
        class TestResource(Resource):
            def post(self):
                return 'test'
        
        api.add_resource(TestResource, '/test')
        
        with app.test_client() as c:
            response = c.post('/test')
            assert response.status_code == 200
            assert response.data == b'"test"\n'
    
    def test_add_resource_with_multiple_routes(self, app):
        api = Api(app)
        
        class TestResource(Resource):
            def get(self):
                return 'test'
        
        api.add_resource(TestResource, '/test', '/test2')
        
        with app.test_client() as c:
            response = c.get('/test')
            assert response.status_code == 200
            assert response.data == b'"test"\n'
            
            response = c.get('/test2')
            assert response.status_code == 200
            assert response.data == b'"test"\n'
    
    def test_add_resource_with_no_supported_method_post(self, app):
        api = Api(app)
        
        class TestResource(Resource):
            def get(self):
                return 'test'
        
        api.add_resource(TestResource, '/test')
        
        with app.test_client() as c:
            response = c.post('/test')
            assert response.status_code == 405
            assert response.data == b'{"message":"Unimplemented method POST"}\n'
    
    def test_add_resource_with_no_supported_method_get(self, app):
        api = Api(app)
        
        class TestResource(Resource):
            def post(self):
                return 'test'
        
        api.add_resource(TestResource, '/test')
        
        with app.test_client() as c:
            response = c.get('/test')
            assert response.status_code == 405
            assert response.data == b'{"message":"Unimplemented method GET"}\n'
    
    def test_add_resource_with_abort_method(self, app):
        api = Api(app)
        
        class TestResource(Resource):
            def get(self):
                abort(499, message="test message")
                return 'test'
        
        api.add_resource(TestResource, '/test')
        
        with app.test_client() as c:
            response = c.get('/test')
            assert response.status_code == 499
            assert response.data == b'{"message":"test message"}\n'
