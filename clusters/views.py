from django.shortcuts import render, get_object_or_404
from django.conf import settings

from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import BarChart, ColumnChart

import readcsv as rc
import readtxt as rt
import pandas as pd
import os


from .models import Cluster

# Create your views here.
def index(request):
    clusters = Cluster.objects.all()
    context = {'clusters': clusters}
    return render(request, 'clusters/index.html', context)

def detail(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    #load csv into pandas.DataFrame
    file_ = open(os.path.join(settings.BASE_DIR, 'clusters/spss.csv'))
    df = pd.read_csv(file_)
    #load questions textfile into list
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/newfile.txt'))
    questions_txt = rt.read(file2_)

    charts = []

    questions_to_show = ['QAGEBND'] #'Q11', 'QGEN', 'QETH'

    for question in questions_to_show:
        dic =  rc.get_data(df, question, questions_txt[question])
        data = dic['data']
        question = dic['question']
        charts.append(BarChart(SimpleDataSource(data=data), options={'title': question, 'isStacked': 'percent'}))


    questions_to_show = ['Q5', 'Q26', 'Q29', 'Q39', 'Q50']
    for question in questions_to_show:
        data =  rc.get_data2(df, question)
        charts.append(BarChart(SimpleDataSource(data=data), options={'title': question}))

    data = rc.get_data_for_column_chart(df)
    charts.append(ColumnChart(SimpleDataSource(data=data), options={'title': "Q13"}))

    context = {
        'cluster': cluster,
        'charts': charts,
    }
    return render(request, 'clusters/detail.html', context)
