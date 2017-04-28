import csv
from flask.ext.script import Command, Option

from connect import settings
from connect.utils.clustering import (
    MAX_DISTANCE_WITHIN_CLUSTER_IN_METERS,
    KM_TO_METERS,
    calculate_centers,
    find_nearby_pairs,
    nearest,
    union_find,
)


CLUSTER_SIZE = 10
DEST_FILENAME = './data/{}.csv'.format(settings.DATA_SET_OUTPUT)
SRC_FILENAME = './data/{}.csv'.format(settings.DATA_SET_TINY)


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

    def build_centers(
        self,
        location_list,
        location_weight_list=None,
        max_distance_within=MAX_DISTANCE_WITHIN_CLUSTER_IN_METERS
    ):
        """
        Uses a minimum spanning tree to perform cluster analysis. Segments the tree into clusters using a distance
        threshold.

        :param list[app.models.base_location.BaseLocation] location_list:
        :param list[float] location_weight_list:
        :param int max_distance_within:
        :return list[dict], list[list[int]]: tuple of (centroids, clusters), where each item in clusters is a cluster, and
            each cluster is a list of indices into location_list.
        """
        if location_weight_list is None:
            location_weight_list = [1] * len(location_list)

            # a list of nearby locations pair (as a tuple)
            # [(loc_1, loc_2), (loc_1, loc_8), (loc_5, loc_6), ...]
            point_pair_list = list(find_nearby_pairs(
                location_list,
                float(max_distance_within) / KM_TO_METERS
            ))

            # Using nearby pairs as the graph link, group locations as clusters
            # [set([loc_1]), set([loc_4, loc_5, loc_8]), ...]
            clusters = union_find(location_list, point_pair_list)

            # calculate the center of each cluster
            #[(lat, lng), (lat, lng), ...]
            centers = calculate_centers(clusters, location_list, location_weight_list)

            # Find the nearest location to the center in the clusters
            centroids = nearest(
                clusters,
                centers,
            )

            # for centroid, cluster in izip(centroids, clusters):
            #     centroid['cluster_size'] = len(cluster)

            # Map locations to indices using location_list order.
            loc_to_idx = {loc: ind for ind, loc in enumerate(location_list)}
            clusters = [[loc_to_idx[loc] for loc in cluster] for cluster in clusters]
            return centroids, clusters

    def run(self, max_distance, file_src, file_dest):
        with open(file_src) as f:
            reader = csv.reader(f, delimiter=',')
            # skip the header
            reader.next()
            locations = []
            for row in reader:
                lat, lng = row
                locations.append((float(lat), float(lng)))
        centers, clusters = self.build_centers(locations, max_distance_within=max_distance)

        with open(file_dest, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['lat', 'lng'])
            for loc in centers:
                writer.writerow(loc)
