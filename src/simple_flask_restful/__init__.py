"""
simple_flask_restful


This library is a lightweight Python package that provides a simpler interface to create RESTful APIs using Flask.
"""

from .simple_restful import Api, Resource
from .restful_exceptions import abort
from . import reqparse
from flask import Flask


__version__ = '0.3.0'
__all__ = ['Api', 'Resource', 'abort', 'reqparse', 'Flask']
