from functools import wraps
from flask import jsonify
from .restful_exceptions import BadRequest, CustomException


def decorator_method(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, BadRequest):
                return jsonify({"message": str(e)}), 400
            elif isinstance(e, CustomException):
                return jsonify({"message": e.message}), e.status_code
            else:
                raise e
        
        if not isinstance(result, tuple) or len(result) != 2 or not isinstance(result[1], int):
            return jsonify(result), 200
        return result
    
    return wrapper
