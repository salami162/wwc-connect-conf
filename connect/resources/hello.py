from flask import request
from flask.ext.restful import Resource

from connect.utils import jsonify_fast as jsonify


class Hello(Resource):
    """A simple resource example."""

    def get(self):
        name = request.args.get('name')

        return jsonify(Hello="World!")
