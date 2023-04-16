# simple_flask_restful

`simple_flask_restful` is a lightweight Python package that provides a simpler interface to create RESTful APIs using Flask.

## Installation

The package can be installed via pip:

`pip3 install simple_flask_restful`

## Usage

The package provides a `Flask` application object and an `Api` object to define the RESTful resources. Here is an example:


```python
from simple_flask_restful import Flask, Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, world!'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
```


In the above example, we define a `HelloWorld` resource that returns a simple JSON message. We add this resource to the `Api` object, which in turn adds it to the `Flask` application object.

### Resources

A resource is a Python class that defines the HTTP methods that are allowed on a particular URL endpoint. Here is an example:

```python
from simple_flask_restful import Flask, Resource, Api, reqparse
class Multiply(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('num1', type=float, required=True)
        self.parser.add_argument('num2', type=float, required=True)

    def get(self):
        args = self.parser.parse_args()
        result = args['num1'] * args['num2']
        return {'result': result}

```

In the above example, we define a `Multiply` resource that expects two query parameters, `numone` and `num2`, and returns their product. We use the `reqparse` module to parse the query parameters.

To add this resource to the `Api` object, we use the `add_resource` method:



`api.add_resource(Multiply, '/multiply', '/product')`

This maps the `Multiply` resource to the `/multiply` and `/multiply` URL endpoint.


**Return Format:** The return of method (get/post/put/delete) in the child class of Resource should be a dictionary or in JSON format. The default HTTP status code is 200. 

**Example:**
`return {'result': result}`
is the same as
`return {'result': result}, 200`


### Running the Server

To run the Flask server, simply call the `run` method on the `Flask` application object:


```python
if __name__ == '__main__':
    app.run(debug=True)
```

This will start the server on port 5000. You can access the resources at their corresponding URL endpoints, for example: `http://localhost:5000/multiply?numone=2&num2=3`.

### reqparse

We are using the `reqparse` module to parse the arguments of the incoming request.

#### add_argument()

`add_argument(name, dest=None, required=False, type=None, choices=None, help=None, default=None)`

This method adds a new argument to the parser.

-   `name`: The name of the argument.
-   `dest`: The name of the attribute to store the argument in. If not specified, `name` will be used.
-   `required`: If `True`, this argument must be included in the request. Defaults to `False`.
-   `type`: The expected data type of the argument. If specified, the argument will be coerced to this type. Supported types include `str`, `int`, `float`, `bool`, and any callable that takes a single string argument and returns the parsed value. If not specified, the argument will be returned as a string.
-   `choices`: A list of valid choices for the argument. If specified, the argument must be one of these choices.
-   `help`: The error message to display if the argument is invalid.
-   `default`: The default value for the argument if it is not included in the request.

#### parse_args()

`parse_args(strict=False)`
This method parses the arguments of the incoming request.

-   `strict`: If `True`, the request must contain only the arguments that were added to the parser. If `False`, additional arguments will be ignored. Defaults to `False`.
## License

`simple_flask_restful` is released under the MIT License.