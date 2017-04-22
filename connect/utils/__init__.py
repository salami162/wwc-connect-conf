import ujson
from flask import Response
from haversine import haversine
from itertools import izip
import csv
from connect.models.location import Location


# Result of haversine((lat+1, lng), (lat, lng)) for all combinations of lat, lng
KILOMETERS_PER_DEGREE_LATITUDE = 111.1338401207391

def read_lat_lng_list_from_file():
    locations = []
    with open('./data/wwc_conf_dataset_tiny.csv') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            loc = Location(
                lat=row['dropoff_lat'],
                lng=row['dropoff_lng']
            )
            locations.append(loc)
    return locations

def jsonify_fast(*args, **kwargs):
    return Response(
        ujson.dumps(dict(*args, **kwargs)),
        mimetype='application/json'
    )


def find_nearby_pairs(items, radius_km):
    """
    Generator that returns all pairs of items whose haversine distance is < radius_km
    This is functionally equivalent to

        for item1, item2 in itertools.combinations(items, 2):
            if haversine((item1.lat, item1.lng), (item2.lat, item2.lng), miles=False) < radius_km:
                yield (item1, item2)

    (although the order of results may differ)
    The elements of items can by of any type that have lat and lng properties.
    This method is almost always faster than (and never slower than) the naive approach; it avoids doing O(N^2)
    haversine calls by earlying out of the inner loop.
    Building an rtree (or similar spatial structure) would reduce the number of haversine checks further, but this
    approach has almost no setup code or memory overhead.
    Note that the worst case occurs when all the items aren't well distributed and have roughly the same
    latitude; in this case, the performance degrades to roughly the same as the naive approach. If this is a concern
    in practice, you should consider an alternative algorithm.

    :param List[Any] items:
    :param float radius_km:
    :rtype: Iterable[Tuple[Any, Any]]
    """
    # Determine the max difference in latitude that will still be within the radius (in km)
    # Dimensional analysis: km / (km / degree) -> degree
    threshold_lat = radius_km / KILOMETERS_PER_DEGREE_LATITUDE

    sorted_items = sorted(items, key=lambda x: x.lat)
    for i, item1 in enumerate(sorted_items):
        for j in xrange(i + 1, len(sorted_items)):
            item2 = sorted_items[j]

            if item2.lat - item1.lat > threshold_lat:
                # All items to the "right" of item2 will be furth than radius_km, so we can break out of the inner loop
                break

            if haversine((item1.lat, item1.lng), (item2.lat, item2.lng), miles=False) < radius_km:
                yield (item1, item2)


def union_find(nodes, edges):
    """
    Find connected components in a graph using the union-find algorithm.

    :param list[collections.Hashable] nodes: list of objects
    :param iter[(collections.Hashable, collections.Hashable)] edges: list of connections between objects
    :return list[list[collections.Hashable]] clusters: list of clusters
    """
    node_clusters = {node: {node} for node in nodes}
    for p1, p2 in edges:

        # Find
        if node_clusters[p1] is node_clusters[p2]:
            continue

        # Get small and large set
        small, large = sorted([node_clusters[p1], node_clusters[p2]], key=len)

        large.update(small)
        for p in small:
            node_clusters[p] = large

    # node_clusters.values() contains each cluster multiple times, de-dupe it
    clusters = node_clusters.itervalues()
    return {id(o): o for o in clusters}.values()


def nearest(clusters, centers):
    """
    Get the location in the input data that is closest to the centroid of each cluster.

    :param list[list[connect.models.location.Location]] clusters:
    :param list[(float, float)] centers:
    :return list[dict]: The closest location for each of the clusters (same length as clusters_by_index).
    """
    nearest_locations = []

    for cluster, center in izip(clusters, centers):
        nearest_location = min(
            cluster,
            key=lambda loc: haversine(center, (loc.lat, loc.lng))
        )
        nearest_locations.append(nearest_location)

    return [loc.to_dict() for loc in nearest_locations]


def calculate_centers(clusters):
    """
    Given a list of clusters, and weights for each location, find the weighted centroid of each cluster.

    :param iter[list[app.models.base_location.BaseLocation]] clusters:
    :param list[app.models.base_location.BaseLocation] base_locations:
    :param list[float] weights: weights[i] corresponds to base_locations[i]
    :return list[(float, float)]: centroids
    """

    center_list = []
    for cluster in clusters:
        lats, lngs, weights = zip(*[(l.lat, l.lng, l.weight) for l in cluster])
        total_weight = sum(weights) or 1
        center_list.append((
            np.dot(lats, weights) / total_weight,
            np.dot(lngs, weights) / total_weight,
        ))

    return center_list
