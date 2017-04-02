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

# from https://www.coursera.org/learn/machine-learning-data-analysis/lecture/XJJz2/running-a-k-means-cluster-analysis-in-python-pt-1
#from https://www.coursera.org/learn/machine-learning-data-analysis/lecture/XJJz2/running-a-k-means-cluster-analysis-in-python-pt-2

def get_elbow_chart_data(data):
    """clus_train must go through get_data() first
    """
    clus_train, serials = _get_clus_train(data)

    clusters=range(1,10)
    meandist=[]


    for k in clusters:
        model=KMeans(n_clusters=k)
        model.fit(clus_train)
        clusassign=model.predict(clus_train)
        meandist.append(sum(np.min(cdist(clus_train, model.cluster_centers_, 'euclidean'), axis=1))
        /clus_train.shape[0])

    '''
    print meandist
    print clusters

    '''
    """
    plt.plot(clusters, meandist)
    plt.xlabel('Number of clusters')
    plt.ylabel('Average distance')
    plt.title('Selecting k with the Elbow Method')
    plt.show()"""

    #format the output for google charts LineCharts
    output = [["clusters", "meandist"]]
    for i in range(len(clusters)):
        output.append([clusters[i], meandist[i]])

    return output

def _get_clus_train(data):

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
    #cluster.describe()

    clustervar = cluster.copy()
    """
    clustervar['Q11']=preprocessing.scale(clustervar['Q11'].astype('float64'))
    clustervar['QGEN']=preprocessing.scale(clustervar['QGEN'].astype('float64'))
    clustervar['QAGEBND']=preprocessing.scale(clustervar['QAGEBND'].astype('float64'))
    clustervar['QETH']=preprocessing.scale(clustervar['QETH'].astype('float64'))
    """

    #clus_train, clus_test = train_test_split(clustervar, test_size=.3, random_state=123)
    return clustervar, data.SERIAL

def get_clustering_chart_data(data):
    clus_train, serials = _get_clus_train(data)

    pca_2 = PCA(2)

    plot_columns = pca_2.fit_transform(clus_train)
    """plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=model5.labels_)
    plt.xlabel('canonical variable 1')
    plt.ylabel('canonical variable 2')
    plt.title('asdf')
    plt.show()"""

    x = plot_columns[:,0]
    y = plot_columns[:,1]
    #c = model5.labels_

    output = [["x", "y"]]
    for i in range(len(x)):
        output.append([x[i], y[i]])

    return output

def get_subcluster_list(cluster, data):
    """
        @cluster Cluster model
        @data pandas.DataFrame object
    """

    num_of_clusters = cluster.num_of_clusters

    clus_train, serials  = _get_clus_train(data)

    if Subcluster.objects.filter(group=cluster).exists():
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

    model5 = KMeans(n_clusters=num_of_clusters)
    model5.fit(clus_train)
    clussassign=model5.predict(clus_train)


    """
    BEGIN multiple steps to merge assignment with clustering variables to examine cluster variable means by cluster
    """
    clus_train.reset_index(level=0, inplace=True)
    cluslist=list(clus_train['index'])
    labels=list(model5.labels_)
    newlist=dict(zip(cluslist, labels))
    #newlist

    newclus=DataFrame.from_dict(newlist, orient='index')
    #newclus

    newclus.columns=['cluster']

    newclus.reset_index(level=0, inplace=True)

    merged_train=pd.merge(clus_train, newclus, on='index')
    #merged_train.head(n=100)

    #merged_train.cluster.value_counts()

    merged_serial = pd.merge(merged_train, serials.to_frame().reset_index(), on='index')

    for i in range(merged_serial.shape[0]):
        row = merged_serial.iloc[i]
        s = Subcluster(serial=row.SERIAL, group=cluster, subcluster=row.cluster)
        s.save()

    #clustergrp=merged_train.groupby('cluster').mean()
    #print "clustering variable means by cluster"
    #print clustergrp
    return merged_train


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


def get_subclusters(cluster, data):
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
    data = get_subcluster_list(cluster, data)
    for i in range(num_of_clusters):
        d[i] = filter_by_subcluster(data, i)
    return d


def filter_by_subcluster(data, subcluster_id):
    """assumes @param data: has gone through get_cluster_list() (has a subcluster column already)
    """
    data = data[(data.cluster == float(subcluster_id))]
    return data
