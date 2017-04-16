MAX_DISTANCE_WITHIN_CLUSTER_IN_METERS = 100


def build_centers(
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
        point_pair_list = list(spatial.find_nearby_pairs(
            location_list,
            float(max_distance_within) / geo.KM_TO_METERS
        ))

        # Using nearby pairs as the graph link, group locations as clusters
        # [set([loc_1]), set([loc_4, loc_5, loc_8]), ...]
        clusters = union_find(location_list, point_pair_list)

        # calculate the center of each cluster
        #[(lat, lng), (lat, lng), ...]
        centers = calculate_centers(clusters)

        # Find the nearest location to the center in the clusters
        centroids = nearest(
            clusters,
            centers,
        )

        for centroid, cluster in izip(centroids, clusters):
            centroid['cluster_size'] = len(cluster)

        # Map locations to indices using location_list order.
        loc_to_idx = {loc: ind for ind, loc in enumerate(location_list)}
        clusters = [[loc_to_idx[loc] for loc in cluster] for cluster in clusters]
        return centroids, clusters
