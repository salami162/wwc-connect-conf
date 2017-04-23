import csv
from random import uniform
from flask.ext.restful import Resource

from connect.utils import jsonify_fast as jsonify
from connect.utils.geojsonify import visualize_as_geojson


class Trained(Resource):
    """Trained data set Resource"""

    def get(self):
        """Return trained data set
        """
        locations = []

        # with open('./data/wwc_conf_dataset_tiny.csv') as f:
        #     csv_reader = csv.DictReader(f)
        #     for row in csv_reader:
        #         loc = [
        #             row['dropoff_lat'],
        #             row['dropoff_lng']
        #         ]
        #         locations.append(loc)
        for i in xrange(15):
            generated_lat = uniform(37.7409, 37.80007)
            generated_lng = uniform(-122.481937, -122.388725)
            locations.append([generated_lat, generated_lng])

        geojson = visualize_as_geojson(locations, sample_scale=1)
        return jsonify(geojson)
