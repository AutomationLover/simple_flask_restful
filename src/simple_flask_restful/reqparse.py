from flask import request
from .restful_exceptions import BadRequest


def get_args_from_request():
    if request.is_json:
        request_args = request.get_json()
    else:
        request_args = request.args.to_dict()
    return request_args


class Parser:
    def __init__(self):
        self.args = []
        self.errors = {}
    
    def add_argument(self, name, dest=None, required=False, type=None, choices=None, help=None, default=None):
        self.args.append({
            'name': name,
            'dest': dest or name,
            'required': required,
            'type': type,
            'choices': choices,
            'help': help,
            'default': default,
        })
    
    def parse_args(self, request_args, strict, bundle_errors):
        args = {}
        self.errors = {}
        
        def error(message, para_name):
            if bundle_errors is False:
                raise BadRequest(message)
            else:
                self.errors[para_name] = message
                
        if strict:
            extra_args = set(request_args.keys()) - set(arg['name'] for arg in self.args)
            if extra_args:
                message = f"Got unexpected arguments: {', '.join(extra_args)}"
                error(message, '_error')
 
        for arg in self.args:
            value = request_args.get(arg['name'], arg.get('default', None))
            if value is None and arg['required']:
                message = f"{arg['name']} is required."
                error(message, arg['name'])
            
            if value is not None:
                if arg['type']:
                    try:
                        value = arg['type'](value)
                    except Exception:
                        message = f"{arg['name']} should be {arg['type'].__name__}."
                        error(message, arg['name'])
                if arg.get('choices') and value not in arg['choices']:
                    message = f"{arg['name']} must be one of {arg['choices']}."
                    error(message, arg['name'])
                    
            args[arg['dest']] = value
        
        if bundle_errors and self.errors:
            raise BadRequest(self.errors)
        return args


class RequestParser(Parser):
    def parse_args(self, strict=False, bundle_errors=False):
        request_args = get_args_from_request()
        return super().parse_args(request_args, strict, bundle_errors)
