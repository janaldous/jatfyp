import pandas as pd
import urllib, json, geojson
from geojson import FeatureCollection
#import superoutputareas as soa



def get_output_areas_from_spss():
    df = pd.read_csv('../spss.csv')

    oa11s = []
    for index, value in df.OA11.value_counts().iteritems():
        oa11s.append(index)
    return oa11s

def write_on_file(oa11s):
    feature_collections = []

    for oa in oa11s:
        url = "http://statistics.data.gov.uk/boundaries/"+oa+".json"
        response = urllib.urlopen(url)
        data = geojson.loads(response.read())
        feature_collections.append(data)

    fc =  FeatureCollection(feature_collections)

    with open('oa11.json', 'w+') as f:
        f.write("%s" % fc)


#main method
#soas = soa.get_super_output_areas_middle()
#write_on_file(soas)
