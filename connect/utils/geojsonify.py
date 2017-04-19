import numpy as np
from colorutils import Color


def visualize_as_geojson(centroids, data, labels, sample_scale=10):
    geojson = {
        'type': 'FeatureCollection',
        'features': []
    }

    colors = np.random.randint(255, size=(len(centroids), 3))
    colors = [Color(tuple(i)).hex for i in colors]

    for i in np.random.choice(len(data), len(data) / sample_scale, replace=False):
        geojson['features'].append({
            'type': 'Feature',
            'properties': {'marker-color': colors[labels[i]]},
            'geometry': {
                'type': 'Point',
                'coordinates': [data[i][1], data[i][0]]
            }
        })

    for i in range(len(centroids)):
        # Add a larger icon for centroids
        geojson['features'].append({
            'type': 'Feature',
            'properties': {'marker-color': colors[i], 'marker-size': 'large', 'marker-symbol': str(i)},
            'geometry': {
                'type': 'Point',
                'coordinates': [centroids[i][1], centroids[i][0]]
            }
        })

    return geojson
