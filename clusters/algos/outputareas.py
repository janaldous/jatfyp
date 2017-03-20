import pandas as pd
import urllib, json, geojson
from geojson import FeatureCollection

df = pd.read_csv('../spss.csv')

idxes = []
for index, value in df.OA11.value_counts().iteritems():
    idxes.append(index)

oa11s = ["E00015359", "E00015761"]
feature_collections = []

for oa in oa11s:
    url = "http://statistics.data.gov.uk/boundaries/"+oa+".json"
    response = urllib.urlopen(url)
    data = geojson.loads(response.read())
    feature_collections.append(data)

print FeatureCollection(feature_collections)
