import csv
from flask.ext.script import Command, Option

from connect.utils.clustering import build_centers

CLUSTER_SIZE = 10
MAX_DISTANCE_WITHIN_CLUSTER_IN_METERS = 100
DEST_FILENAME = './data/trained_output.csv'
SRC_FILENAME = './data/wwc_conf_dataset_tiny.csv'


class HierarchyCommand(Command):
    def __init__(self, cluster_size=CLUSTER_SIZE, file_src=SRC_FILENAME, file_dest=DEST_FILENAME):
        self.cluster_size = cluster_size
        self.file_src = file_src
        self.file_dest = file_dest

    def get_options(self):
        return [
            Option('-m_dist', '--max_distance', dest='max_distance', default=MAX_DISTANCE_WITHIN_CLUSTER_IN_METERS),
            Option('-src', '--source_file', dest='file_src', default=self.file_src),
            Option('-dest', '--dest_file', dest='file_dest', default=self.file_dest)
        ]

    def run(self, max_distance, file_src, file_dest):
        with open(file_src) as f:
            reader = csv.reader(f, delimiter=',')
            # skip the header
            reader.next()
            locations = []
            for row in reader:
                lat, lng = row
                locations.append((float(lat), float(lng)))
        centers, clusters = build_centers(locations, max_distance_within=max_distance)

        with open(file_dest, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['dropoff_lat', 'dropoff_lng'])
            for loc in centers:
                writer.writerow(loc)
