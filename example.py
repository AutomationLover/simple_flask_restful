from simple_flask_restful import (Flask,
                                  reqparse,
                                  Resource,
                                  Api, abort)

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, world!'}


class Multiply(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('num1', type=float, required=True)
        self.parser.add_argument('num2', type=float, required=True)

    def get(self):
        args = self.parser.parse_args()
        result = args['num1'] * args['num2']
        return {'result': result}


class Calculator(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('num1', type=float, required=True)
        self.parser.add_argument('num2', type=float, required=True)

    def get(self):
        args = self.parser.parse_args()
        result = args['num1'] + args['num2']
        return {'result': result}

    def post(self):
        args = self.parser.parse_args()
        result = args['num1'] - args['num2']
        return {'result': result}


class Abort(Resource):
    def get(self):
        abort(400, message="This is an error message.")


class NotRealizedMethod(Resource):
    def put(self):
        return {'message': 'This is a PUT request.'}


api.add_resource(HelloWorld, '/')
api.add_resource(Multiply, '/multiply')
api.add_resource(Calculator, '/calculator', '/addition')
api.add_resource(Abort, '/abort')
api.add_resource(NotRealizedMethod, '/not-realized-method')


if __name__ == '__main__':
    app.run(debug=True)
