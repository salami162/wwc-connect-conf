from flask import Flask
from flask.ext import restful

from connect import settings


app = Flask(__name__)
app.config.from_object(settings)
api = restful.Api(app)


@app.route('/healthcheck')
def healthcheck():
    # The healthcheck returns status code 200
    return 'OK'

from connect import resources  # noqa
