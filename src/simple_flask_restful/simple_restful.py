from flask import request, jsonify
from .decorator_method import decorator_method


class Api:
    """
    A class representing a RESTful API.
    """

    def __init__(self, app):
        """
        Constructor for the Api class.

        :param app: The Flask application to which the API will be added.
        """
        self.app = app
        self.resources = {}

    def add_resource(self, resource_class, *routes):
        """
        Adds a resource to the API.

        :param resource_class: The class of the resource to add.
        :param routes: One or more URL routes to associate with the resource.
        """
        resource = resource_class()
        endpoint = resource.class_name.lower()

        for i, route in enumerate(routes):
            self.resources[route] = resource
            self.app.add_url_rule(
                route,
                view_func=resource.as_view(endpoint+str(i)),
                methods=resource.methods
            )


class Resource:
    """
    A base class for RESTful resources.
    """
    methods = {"GET", "POST", "PUT", "DELETE"}

    @property
    def class_name(self):
        return str(self.__class__.__name__)
    
    def dispatch_request(self, *args, **kwargs):
        """
        Dispatches a request to the appropriate method on the resource.

        :param args: Positional arguments to pass to the method.
        :param kwargs: Keyword arguments to pass to the method.
        """
        request_method = request.method
        meth = getattr(self, request_method.lower(), None)
        if meth is None and request_method == 'HEAD':
            meth = getattr(self, 'get', None)
        if meth is None:
            return jsonify({"message": f'Unimplemented method {request_method}'}), 405

        meth = decorator_method(meth)
        return meth(*args, **kwargs)

    def as_view(self, endpoint):
        """
        Returns a Flask view function for the resource.

        :param endpoint: The endpoint name for the view function.
        """
        def view(*args, **kwargs):
            return self.dispatch_request(*args, **kwargs)

        # Add the methods to the view function
        for method in self.methods:
            view.__dict__[method.lower()] = True
        view.__name__ = endpoint  # Flask can generate URLs for the endpoint based on its name.
        return view
