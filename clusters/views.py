from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse

from .forms import ClusterForm
from .models import Cluster

from graphosjat.sources.simple import SimpleDataSource
from graphosjat.renderers.gchart import BarChart, ColumnChart, StackedBarChart

from random import randint

import readcsv as rc
import readcsv2 as rc2
import readtxt as rt
import pandas as pd
import os


# Create your views here.
def index(request):
    clusters = Cluster.objects.all()
    context = {'clusters': clusters}
    return render(request, 'clusters/index.html', context)

def map(request):
    return render(request, 'clusters/map.html')

def test(request):
    return render(request, 'clusters/test.html')

def json(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    #load csv into pandas.DataFrame
    file_ = open(os.path.join(settings.BASE_DIR, 'clusters/spss.csv'))
    dic = rc.filter_by_cluster(pd.read_csv(file_), cluster)
    df = dic['df']

    output = rc2.get_data_for_map(df, 'WARD')

    return JsonResponse(output, safe=False)

def json2(request, cluster_id, question_id, choice_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    #load csv into pandas.DataFrame
    file_ = open(os.path.join(settings.BASE_DIR, 'clusters/spss.csv'))
    dic = rc.filter_by_cluster(pd.read_csv(file_), cluster)
    df = dic['df']

    output = rc2.get_data_for_map2(df, question_id, choice_id)

    return JsonResponse(output, safe=False)

def json3(request, cluster_id, question_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    #load csv into pandas.DataFrame
    file_ = open(os.path.join(settings.BASE_DIR, 'clusters/spss.csv'))
    dic = rc.filter_by_cluster(pd.read_csv(file_), cluster)
    df = dic['df']

    output = rc2.get_data_for_map3(df, question_id)

    return JsonResponse(output, safe=False)

def detail(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    #load csv into pandas.DataFrame
    file_ = open(os.path.join(settings.BASE_DIR, 'clusters/spss.csv'))
    dic = rc.filter_by_cluster(pd.read_csv(file_), cluster)
    df = dic['df']
    size_str = "%d / %d" % (len(df.index), dic['orig_size'])
    #load questions textfile into list
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt'))
    dic_source = rt.read(file2_)
    about = dic_source['about']
    questions_txt = dic_source['questions']

    #get cluster questions as strings
    questions_strs = get_questions_as_str(questions_txt)

    #get charts
    charts = get_charts(df, questions_txt)

    context = {
        'cluster': cluster,
        'charts': charts,
        'df_size': size_str,#no of rows in df
        'questions_strs': questions_strs,
        'about': about,
    }
    return render(request, 'clusters/detail.html', context)

def compare(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    clusterAll = get_object_or_404(Cluster, pk=3)
    #load csv into pandas.DataFrame
    file_ = open(os.path.join(settings.BASE_DIR, 'clusters/spss.csv'))
    dicAll = rc.filter_by_cluster(pd.read_csv(file_), clusterAll)
    dic = rc.filter_by_cluster(dicAll['df'], cluster)
    df = dic['df']
    size_str = "%d / %d" % (len(df.index), dic['orig_size'])
    #load questions textfile into list
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt'))
    dic_source = rt.read(file2_)
    about = dic_source['about']
    questions_txt = dic_source['questions']

    #get cluster questions as strings
    questions_strs = get_questions_as_str(questions_txt)

    #get charts
    charts = get_charts_compare(df, dicAll['df'], questions_txt)

    context = {
        'cluster': cluster,
        'charts': charts,
        'df_size': size_str,#no of rows in df
        'questions_strs': questions_strs,
        'about': about,
    }
    return render(request, 'clusters/compare.html', context)

def create_cluster(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ClusterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ClusterForm()

    return render(request, 'clusters/form.html', {'form': form})

def survey_questions(request):
    #load csv
    file_ = open(os.path.join(settings.BASE_DIR, 'clusters/spss.csv'))
    df = pd.read_csv(file_)
    #load questionchoices txt
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt'))
    dic_source = rt.read(file2_)
    about = dic_source['about']
    questions_txt = dic_source['questions']

    context = {
        'questions': questions_txt.values(),
        'about': about,
    }
    return render(request, 'clusters/survey.html', context)

def see_question_answers(request, question):
    #load csv
    file_ = open(os.path.join(settings.BASE_DIR, 'clusters/spss.csv'))
    df = pd.read_csv(file_)
    #load questionchoices txt
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt'))
    dic_source = rt.read(file2_)
    about = dic_source['about']
    questions_txt = dic_source['questions']

    chart = get_question_chart(df, questions_txt[question])

    context = {
        'chart': chart,
        'question': question,
        'about': about,
    }
    return render(request, 'clusters/question.html', context)

def get_question_chart(df, question_obj):
    dic = rc.get_data_for_question(df, question_obj)
    data = dic['data']
    question = dic['question']
    chart = BarChart(SimpleDataSource(data=data), options={'title': question, 'isStacked': 'percent'})
    return chart


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

def get_charts(df, questions_txt):
    charts = []

    #Single code quesitions
    questions_to_show = ['WARD','Q11', 'QGEN', 'QAGEBND', 'QETH', 'Q34']

    for question in questions_to_show:
        dic =  rc.get_data_for_stacked_bar_charts(df, questions_txt[question])
        data = dic['data']
        question = dic['question']
        charts.append(StackedBarChart(SimpleDataSource(data=data), options={'title': question, 'isStacked': 'percent', 'height': 100, 'width': 1100, 'legend': { 'position': 'bottom', 'maxLines': '3' }}))


    #multicode questions
    questions_to_show = ['Q5', 'Q26', 'Q29', 'Q39', 'Q50']
    for question in questions_to_show:
        dic =  rc.get_data_for_bar_charts(df, questions_txt[question])
        data = dic['data']
        question = dic['question']
        options={
            'title': question,
            }
        charts.append(BarChart(SimpleDataSource(data=data), options=options))

    dic =  rc.get_data_for_column_chart(df, questions_txt['Q13'])
    data = dic['data']
    question = dic['question']
    charts.append(ColumnChart(SimpleDataSource(data=data), options={'title': question}))

    return charts

def get_charts_compare(df, dfAll, questions_txt):
    charts = []

    #Single code quesitions
    questions_to_show = ['WARD','Q11', 'QGEN', 'QAGEBND', 'QETH', 'Q34']

    for question in questions_to_show:
        dic =  rc2.get_data_for_stacked_bar_charts2(df, dfAll, questions_txt[question])
        data = dic['data']
        question = dic['question']
        charts.append(StackedBarChart(SimpleDataSource(data=data), options={'title': question, 'isStacked': 'percent', 'height': 200, 'width': 1100, 'legend': { 'position': 'bottom', 'maxLines': '3' }}))


    #multicode questions
    questions_to_show = ['Q5', 'Q26', 'Q29', 'Q39', 'Q50']
    for question in questions_to_show:
        dic =  rc2.get_data_for_bar_charts2(df, dfAll, questions_txt[question])
        data = dic['data']
        question = dic['question']
        options={
            'title': question,
            }
        charts.append(BarChart(SimpleDataSource(data=data), options=options))

    dic =  rc2.get_data_for_column_chart2(df, questions_txt['Q13'])
    data = dic['data']
    question = dic['question']
    charts.append(ColumnChart(SimpleDataSource(data=data), options={'title': question}))

    return charts
