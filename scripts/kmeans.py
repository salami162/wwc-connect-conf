import numpy as np
from flask.ext.script import Command, Option
from sklearn.cluster import KMeans

CLUSTER_SIZE = 10
DEST_FILENAME = './data/trained_output.csv'
SRC_FILENAME = './data/wwc_conf_dataset_tiny.csv'


class KMeansCommand(Command):
    def __init__(self, cluster_size=CLUSTER_SIZE, file_src=SRC_FILENAME, file_dest=DEST_FILENAME):
        self.cluster_size = cluster_size
        self.file_src = file_src
        self.file_dest = file_dest

    def get_options(self):
        return [
            Option('-c', '--cluster_size', dest='cluster_size', default=self.cluster_size),
            Option('-src', '--source_file', dest='file_src', default=self.file_src),
            Option('-dest', '--dest_file', dest='file_dest', default=self.file_dest)
        ]

    def run(self, cluster_size, file_src, file_dest):
        try:
            cluster_size = int(cluster_size)
        except TypeError:
            print "please enter a number for cluster size"
        locations = np.genfromtxt(file_src, delimiter=',', skip_header=1)
        centers = KMeans(n_clusters=cluster_size, random_state=0).fit(locations)
        np.savetxt(file_dest, centers.cluster_centers_, delimiter=",", header='dropoff_lat,dropoff_lng', fmt="%5f")
