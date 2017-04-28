import json
import pandas
from sklearn.cluster import KMeans


def read_data(dataset='wwc_conf_dataset.csv'):
    return pandas.read_csv(dataset)


def convert_data_for_sklearn(df):
    data = []
    for i, row in df.iterrows():
        data.append([row['lat'], row['lng']])
    return data


def kmeans(data, k=18):
    model = KMeans(n_clusters=k)
    model.fit(data)
    centroids = model.cluster_centers_
    labels = model.predict(data)
    return centroids, labels


def write_data_csv():
    df = read_data()
    data = convert_data_for_sklearn(df)
    centroids, labels = kmeans(data)

    with open('./../data/output_kmean', 'w') as f:
        json.dump(centroids, data, labels, f, sort_keys=True, indent=4)
        # pandas.write_data_csv(centroids, data, labels)
