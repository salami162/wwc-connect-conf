from connect import api
from connect.resources.hello import Hello
from connect.resources.destinations import Destinations

# Add your resources here
api.add_resource(Hello, '/v1/hello')
api.add_resource(Destinations, '/v1/destinations')
