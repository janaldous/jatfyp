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
    dic = rc.filter_by_cluster(pd.read_csv(file_), cluster)
    df = dic['df']
    size_str = "%d / %d" % (len(df.index), dic['orig_size'])
    #load questions textfile into list
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt'))
    questions_txt = rt.read(file2_)

    #get cluster questions as strings
    questions_strs = get_questions_as_str(questions_txt)

    charts = []

    questions_to_show = ['Q11', 'QGEN', 'QAGEBND', 'QETH']

    for question in questions_to_show:
        dic =  rc.get_data(df, questions_txt[question])
        data = dic['data']
        question = dic['question']
        charts.append(BarChart(SimpleDataSource(data=data), options={'title': question, 'isStacked': 'percent', 'height': 100, 'legend': { 'position': 'bottom', 'maxLines': '3' }}))


    questions_to_show = ['Q5', 'Q26', 'Q29', 'Q39', 'Q50']
    for question in questions_to_show:
        dic =  rc.get_data2(df, questions_txt[question])
        data = dic['data']
        question = dic['question']
        charts.append(BarChart(SimpleDataSource(data=data), options={'title': question}))

    dic =  rc.get_data_for_column_chart(df, questions_txt['Q13'])
    data = dic['data']
    question = dic['question']
    charts.append(ColumnChart(SimpleDataSource(data=data), options={'title': question}))

    context = {
        'cluster': cluster,
        'charts': charts,
        'df_size': size_str,#no of rows in df
        'questions_strs': questions_strs,
    }
    return render(request, 'clusters/detail.html', context)

def get_questions_as_str(questions_txt):
    '''
        not a view
    '''
    questions = ['Q43', 'Q45', 'Q46', 'Q47', 'Q35']
    questions_strs = []
    for question in questions:
        qstr = questions_txt[question].question
        questions_strs.append(qstr)
    return questions_strs
