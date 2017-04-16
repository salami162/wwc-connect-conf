from connect import api
from connect.resources.hello import Hello

# Add your resources here
api.add_resource(Hello, '/v1/hello')
