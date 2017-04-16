import itertools
import pytest
import random

from haversine import haversine

from connect.models.location import Location
from connect.utils import find_nearby_pairs, union_find, nearest
from tests.unit import fixtures


class DummyItem(object):

    def __init__(self, lat, lng, index):
        self.lat = lat
        self.lng = lng
        self.index = index


class TestUtils():

    def _generate_locations(self, loc_data):
        data = []
        for lat, lng, name in loc_data:
            data.append(Location(**{
                'lat': lat,
                'lng': lng,
                'name': name
            }))
        return data

    def _find_nearby_pairs_brute_force(self, items, radius_km):
        for item1, item2 in itertools.combinations(items, 2):
            if haversine((item1.lat, item1.lng), (item2.lat, item2.lng), miles=False) < radius_km:
                yield (item1, item2)

    def test_find_nearby_pairs(self):
        rng = random.Random(1234)

        # Generate some sample points in SFO
        min_lat = 37.7312
        min_lng = -122.477
        max_lat = 37.8122
        max_lng = -122.3665

        items = []
        for i in range(100):
            lat = rng.uniform(min_lat, max_lat)
            lng = rng.uniform(min_lng, max_lng)
            items.append(DummyItem(lat, lng, i))

        for r in [.01, .1, 1, 10]:
            naive_overlaps = self._find_nearby_pairs_brute_force(items, r)
            optimized_overlaps = find_nearby_pairs(items, r)

            # Make sure we get the same results
            # Since we want to consider e.g. (1, 3) and (3, 1) as the same result, sort the indices
            naive_comparable = [tuple(sorted([a.index, b.index])) for a, b in naive_overlaps]
            optimized_comparable = [tuple(sorted([a.index, b.index])) for a, b in optimized_overlaps]
            assert set(naive_comparable) == set(optimized_comparable)

            if r == 10:
                # Ensure we at least got some results to compare
                assert len(optimized_comparable) != 0

    def test_union_find_1(self):
        """
        Example from slide 14 of
        https://www.cs.princeton.edu/~rs/AlgsDS07/01UnionFind.pdf
        """
        centroid_edge_list = [
            (3, 4),
            (4, 9),
            (8, 0),
            (2, 3),
            (5, 6),
            (5, 9),
            (7, 3),
            (4, 8),
            (6, 1),
        ]

        expected_clusters = [set(range(10))]

        clusters = union_find(range(10), centroid_edge_list)
        assert clusters == expected_clusters

    def test_union_find_2(self):
        """
        Example from slide 20 of
        https://www.cs.princeton.edu/~rs/AlgsDS07/01UnionFind.pdf
        """
        centroid_edge_list = [
            (0, 1),
            (2, 3),
            (4, 5),
            (6, 7),
            (7, 8),
            (8, 9),
        ]

        expected_clusters = [set([0, 1]), set([2, 3]), set([4, 5]), set([8, 9, 6, 7])]

        clusters = union_find(range(10), centroid_edge_list)

        assert sorted(clusters, key=sorted) == sorted(expected_clusters, key=sorted)

    @pytest.mark.parametrize('test_center, expected_centroid_ind', [
        ((37.7603392, -122.412672), 0),
        ((37.760458, -122.412701), 1),
        ((37.760339, -122.41267), 0),
    ])
    def test_nearest(self, test_center, expected_centroid_ind):
        loc_data = [fixtures.LYFT_HQ, fixtures.LYFT_HQ_NEARBY, fixtures.ATT]
        location_list = self._generate_locations(loc_data)

        clusters = [[location_list[0], location_list[1]], [location_list[2]]]

        centers = [test_center, (0, 0)]

        centroid_list = nearest(clusters, centers)

        expected_centroid_list = [location_list[expected_centroid_ind], location_list[2]]
        expected_centroid_list = [c.to_dict() for c in expected_centroid_list]

        assert centroid_list == expected_centroid_list
