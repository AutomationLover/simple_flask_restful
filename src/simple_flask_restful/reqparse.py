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

    def parse_args(self, request_args, strict):
        args = {}
        if strict:
            extra_args = set(request_args.keys()) - set(arg['name'] for arg in self.args)
            if extra_args:
                raise BadRequest(f"Got unexpected arguments: {', '.join(extra_args)}")
    
        for arg in self.args:
            value = request_args.get(arg['name'], arg.get('default', None))
            if value is None and arg['required']:
                raise BadRequest(f"{arg['name']} is required.")
        
            if value is not None:
                if arg['type']:
                    try:
                        value = arg['type'](value)
                    except Exception:
                        message = f"{arg['name']} should be {arg['type'].__name__}."
                        raise BadRequest(message)
                if arg.get('choices') and value not in arg['choices']:
                    raise BadRequest(f"{arg['name']} must be one of {arg['choices']}.")
            args[arg['dest']] = value
        return args


class RequestParser(Parser):
    def parse_args(self, strict=False):
        request_args = get_args_from_request()
        return super().parse_args(request_args, strict)
    
