from flask import request
from flask.ext.restful import Resource


class Hello(Resource):
    """A simple resource example."""

    def get(self):
        name = request.args.get('name')
        return {"Hello": "World!"}
