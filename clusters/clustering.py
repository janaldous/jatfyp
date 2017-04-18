from pandas import Series, DataFrame
import pandas as pd
import numpy as np
#import matplotlib.pylab as plt
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.cluster import KMeans

from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA

from .models import Subcluster

from kmodes import kmodes

columns = ['WARD', 'Q11', 'QGEN', 'QAGEBND', 'QETH', 'Q34']

def get_elbow_chart_data(data):
    """clus_train must go through get_data() first
    """
    # adapted from https://www.coursera.org/learn/machine-learning-data-analysis/lecture/XJJz2/running-a-k-means-cluster-analysis-in-python-pt-1

    clus_train, serials = _get_clus_train(data)

    clusters=range(1,10)
    meandist=[]


    for k in clusters:
        model=KMeans(n_clusters=k)
        model.fit(clus_train)
        clusassign=model.predict(clus_train)
        meandist.append(sum(np.min(cdist(clus_train, model.cluster_centers_, 'euclidean'), axis=1))
        /clus_train.shape[0])

    #format the output for google charts LineCharts
    output = [["clusters", "meandist"]]
    for i in range(len(clusters)):
        output.append([clusters[i], meandist[i]])

    return output

def _get_clus_train(data):
    global columns
    columns = ['WARD', 'Q11', 'QGEN', 'QAGEBND', 'QETH', 'Q34']
    for i in range(1,9):
        columns.append('Q13_R'+str(i))
    #append other columns
    import string
    uc = string.ascii_uppercase
    for i in range(0,len(uc)):
        try:
            c = data['Q50'+uc[i]]
            columns.append('Q50'+uc[i])
        except KeyError:
            break

    cluster=data[columns]
    clustervar = cluster.copy()

    return clustervar, data.SERIAL

def get_clustering_chart_data(data):
    clus_train, serials = _get_clus_train(data)

    pca_2 = PCA(2)

    plot_columns = pca_2.fit_transform(clus_train)

    x = plot_columns[:,0]
    y = plot_columns[:,1]

    output = [["x", "y"]]
    for i in range(len(x)):
        output.append([x[i], y[i]])

    return output

def get_table_data(cluster, data):
    query_results = Subcluster.objects.filter(group=cluster)
    serials = []
    subclusters = []
    for row in query_results:
        serials.append(float(row.serial))
        subclusters.append(row.subcluster)
    df = pd.DataFrame(
        {'SERIAL': serials,
         'cluster': subclusters,
        })

    data = data[data['SERIAL'].isin(df.SERIAL.tolist())]
    merged_db = pd.merge(df, data, on='SERIAL')

    merged_db = merged_db[columns+['cluster']]

    return merged_db.groupby('cluster').mean()

def get_subcluster_list(cluster, data, norefresh=True):
    """
        @cluster Cluster model
        @data pandas.DataFrame object

        adapted from https://github.com/nicodv/kmodes/blob/master/examples/soybean.py
    """

    num_of_clusters = cluster.num_of_clusters

    clus_train, serials  = _get_clus_train(data)

    if Subcluster.objects.filter(group=cluster).exists() and norefresh:
        #make dataframe from db
        query_results = Subcluster.objects.filter(group=cluster)
        serials = []
        subclusters = []
        for row in query_results:
            serials.append(float(row.serial))
            subclusters.append(row.subcluster)
        df = pd.DataFrame(
            {'SERIAL': serials,
             'cluster': subclusters,
            })

        data = data[data['SERIAL'].isin(df.SERIAL.tolist())]
        merged_db = pd.merge(df, data, on='SERIAL')

        return merged_db

    Subcluster.objects.filter(group=cluster).delete()

    x = clus_train.as_matrix()

    kmodes_huang = kmodes.KModes(n_clusters=num_of_clusters, init='Huang', verbose=1)
    kmodes_huang.fit(x)

    labels = kmodes_huang.labels_

    clus_train['cluster'] = labels

    clus_train['SERIAL'] = serials

    for i in range(clus_train.shape[0]):
        row = clus_train.iloc[i]
        s = Subcluster(serial=row.SERIAL, group=cluster, subcluster=row.cluster)
        s.save()

    return clus_train


def get_subclusters_length(cluster, data):
    """
        @param cluster: models.cluster object
        @param data: pandas.DataFrame object, filtered by cluster already
        @return dicitonary{subcluster_id: length of df of subcluster}
    """
    # check if cluster.num_of_clusters == 0, set default to 3
    if cluster.num_of_clusters == 0:
        cluster.num_of_clusters = 1
        cluster.save()

    num_of_clusters = cluster.num_of_clusters
    d = {}
    data = get_subcluster_list(cluster, data)
    for i in range(num_of_clusters):
        d[i] = len(filter_by_subcluster(data, i).index)
    return d


def get_subclusters(cluster, data, refresh=False):
    """
        @param cluster: models.Cluster object
        @param data: pandas.DataFrame filtered by cluster already
        @return dictionary{subcluster_id: df(in the form of pandas.DataFrame)}
    """
    # check if cluster.num_of_clusters == 0, set default to 1
    if cluster.num_of_clusters == 0:
        cluster.num_of_clusters = 1
        cluster.save()

    num_of_clusters = cluster.num_of_clusters
    d = {}
    data = get_subcluster_list(cluster, data, norefresh=(not refresh))
    for i in range(num_of_clusters):
        d[i] = filter_by_subcluster(data, i)
    return d

def filter_by_subcluster(data, subcluster_id):
    """assumes @param data: has gone through get_cluster_list() (has a subcluster column already)
    """
    data = data[(data.cluster == float(subcluster_id))]
    return data
