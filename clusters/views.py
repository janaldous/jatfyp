from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse

from .forms import ClusterForm
from .models import Cluster

from graphosjat.sources.simple import SimpleDataSource
from graphosjat.renderers.gchart import BarChart, ColumnChart, StackedBarChart, \
PieChart, LineChart, ScatterChart

from random import randint

import readcsv as rc
import readcsv2 as rc2
import readtxt as rt
import pandas as pd
import os
import clustering
import utils

dataframeAll = pd.read_csv(open(os.path.join(settings.BASE_DIR, 'clusters/spss.csv')))

# Create your views here.
def index(request):
    clusters = Cluster.objects.all()
    context = {'clusters': clusters}
    return render(request, 'clusters/index.html', context)

def compare_maps(request):
    return render(request, 'clusters/compare_maps.html')

def map(request):
    return render(request, 'clusters/map.html')

def test(request):
    return render(request, 'clusters/tests/test.html')

def subclusters_list(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    dic = rc.filter_by_cluster(dataframeAll, cluster)
    clusters_dict = clustering.get_subclusters(cluster, dic['df'])
    context = {
        'cluster_id': cluster_id,
        'subcluster_values': list(clusters_dict.values()),
        }
    return render(request, 'clusters/subcluster_list.html', context)

def subcluster_detail(request, cluster_id, subcluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    #load csv into pandas.DataFrame
    dic = rc.filter_by_cluster(utils.get_whole_survey(), cluster)
    df = dic['df']
    df = clustering.get_subclusters(cluster, df)[0]#dicitonary

    size_str = "%d / %d" % (len(df.index), dic['orig_size'])
    clusters_dict = clustering.get_subclusters_length(cluster, dic['df'])
    #load questions textfile into list
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt'))
    dic_source = rt.read(file2_)
    about = dic_source['about']
    questions_txt = dic_source['questions']
    file2_.close()

    #get cluster questions as strings
    questions_strs = get_questions_as_str(questions_txt)

    #get charts
    charts = get_charts(df, questions_txt, cluster, subcluster_id)

    context = {
        'cluster': cluster,
        'subcluster_id': subcluster_id,
        'charts': charts,
        'df_size': size_str,#no of rows in df
        'questions_strs': questions_strs,
        'about': about,
        'subcluster_values': list(clusters_dict.values()),
        'num_of_clusters': cluster.num_of_clusters,
    }
    return render(request, 'clusters/detail.html', context)

def json(request, cluster_id):
    """ used for map """
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    #load csv into pandas.DataFrame
    dic = rc.filter_by_cluster(utils.get_whole_survey(), cluster)
    df = dic['df']

    #load questions textfile into list
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt'))
    dic_source = rt.read(file2_)
    about = dic_source['about']
    questions_txt = dic_source['questions']
    file2_.close()

    output = rc2.get_data_for_map(df, questions_txt['WARD'])

    return JsonResponse(output, safe=False)

def jsonv2(request, cluster_id):
    """ used for Ward chart """
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    #load csv into pandas.DataFrame
    dic = rc.filter_by_cluster(utils.get_whole_survey(), cluster)
    df = dic['df']

    #load questions textfile into list
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt'))
    dic_source = rt.read(file2_)
    about = dic_source['about']
    questions_txt = dic_source['questions']
    file2_.close()

    output = rc2.get_data_for_mapv2(df, questions_txt['WARD'])

    return JsonResponse(output, safe=False)

def json2(request, cluster_id, subcluster_id, question_id, choice_id):
    """ creates json for map change
    """
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    #load csv into pandas.DataFrame
    dic = rc.filter_by_cluster(utils.get_whole_survey(), cluster)
    df = dic['df']

    if subcluster_id != 'a': #if is subcluster, then filter subcluster
        tempdf = clustering.get_subcluster_list(cluster, df)
        df = clustering.filter_by_subcluster(tempdf, subcluster_id)

    output = rc2.get_data_for_map2(df, question_id, choice_id)

    return JsonResponse(output, safe=False)

def json3(request, cluster_id, question_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    #load csv into pandas.DataFrame
    dic = rc.filter_by_cluster(utils.get_whole_survey(), cluster)
    df = dic['df']

    output = rc2.get_data_for_map3(df, question_id)

    return JsonResponse(output, safe=False)

def json4(request, cluster_id, subcluster_id, question_id, choice_id):
    """for ward chart change
    """
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    #load csv into pandas.DataFrame
    df = rc.filter_by_cluster_only(utils.get_whole_survey(), cluster)

    if subcluster_id != 'a': #if is subcluster, then filter subcluster
        #TODO need to make permanent, subcluster id on df
        tempdf = clustering.get_subcluster_list(cluster, df)
        df = clustering.filter_by_subcluster(tempdf, subcluster_id)

    output = rc2.get_data_for_map4(df, question_id, choice_id)

    return JsonResponse(output, safe=False)

def jsoncompare(request, question_id, choice_id):
    output = rc2.get_data_for_group_compare(question_id, choice_id)

    return JsonResponse(output, safe=False)

def stats(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    cluster_df = utils.get_cluster_from_whole_survey(cluster)
    clusters_dict = clustering.get_subclusters_length(cluster, cluster_df)

    elbow_data = clustering.get_elbow_chart_data(cluster_df)
    elbow_chart = LineChart(SimpleDataSource(data=elbow_data), options={'width':420, 'title': 'Elbow chart', 'legend': {'position': 'bottom'}})

    scatter_data = clustering.get_clustering_chart_data(cluster_df)
    scatter_chart = ScatterChart(SimpleDataSource(data=scatter_data), options={'width':420, 'title': '2d representation of data', 'legend': {'position': 'none'}})

    subcluster_values = list(clusters_dict.values())

    total_pop = utils.get_survey_num_of_rows()
    percentage = (float(cluster_df.shape[0])/float(total_pop))*100

    context = {
        'cluster': cluster,
        'subcluster_values': subcluster_values,
        'num_of_clusters': cluster.num_of_clusters,
        'total_group_pop': cluster_df.shape[0],
        'elbow_chart': elbow_chart,
        'scatter_chart': scatter_chart,
        'total_pop': total_pop,
    }

    return render(request, 'clusters/stats.html', context)

def group_compare(request):
    cluster = get_object_or_404(Cluster, pk=3)
    #load csv into pandas.DataFrame
    dic = rc.filter_by_cluster(utils.get_whole_survey(), cluster)
    df = dic['df']
    size_str = "%d / %d" % (len(df.index), dic['orig_size'])
    clusters_dict = clustering.get_subclusters_length(cluster, dic['df'])
    #load questions textfile into list
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt'))
    dic_source = rt.read(file2_)
    about = dic_source['about']
    questions_txt = dic_source['questions']
    file2_.close()

    #get cluster questions as strings
    questions_strs = get_questions_as_str(questions_txt)

    #get charts
    charts = get_charts(df, questions_txt, cluster, 'a')


    context = {
        'cluster': cluster,
        'charts': charts,
        #'compare_chart': compare_chart,
        'df_size': size_str,#no of rows in df
        'questions_strs': questions_strs,
        'about': about,
        'subcluster_values': list(clusters_dict.values()),
        'num_of_clusters': cluster.num_of_clusters,
        'compare': False,
    }
    return render(request, 'clusters/group_compare.html', context)

def detail(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    #load csv into pandas.DataFrame
    dic = rc.filter_by_cluster(utils.get_whole_survey(), cluster)
    df = dic['df']
    group_size = len(df.index)
    survey_size = dic['orig_size']
    clusters_dict = clustering.get_subclusters_length(cluster, dic['df'])
    #load questions textfile into list
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt'))
    dic_source = rt.read(file2_)
    file2_.close()
    about = dic_source['about']
    questions_txt = dic_source['questions']

    #get cluster questions as strings
    questions_strs = get_questions_as_str(questions_txt)

    #get charts
    charts = get_charts(df, questions_txt, cluster, 'a')


    context = {
        'cluster': cluster,
        'subcluster_id': 'a',
        'charts': charts,
        'group_size': group_size,#no of rows in df
        'survey_size': survey_size,
        'questions_strs': questions_strs,
        'about': about,
        'subcluster_values': list(clusters_dict.values()),
        'num_of_clusters': cluster.num_of_clusters,
        'compare': False,
    }
    return render(request, 'clusters/detail.html', context)

def compare(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    clusterAll = get_object_or_404(Cluster, pk=3)
    #load csv into pandas.DataFrame
    dicAll = rc.filter_by_cluster(utils.get_whole_survey(), clusterAll)
    dic = rc.filter_by_cluster(dicAll['df'], cluster)
    df = dic['df']
    size_str = "%d / %d" % (len(df.index), dic['orig_size'])
    clusters_dict = clustering.get_subclusters_length(cluster, dic['df'])
    #load questions textfile into list
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt'))
    dic_source = rt.read(file2_)
    file2_.close()
    about = dic_source['about']
    questions_txt = dic_source['questions']

    #get cluster questions as strings
    questions_strs = get_questions_as_str(questions_txt)

    #get charts
    charts = get_charts_compare(df, dicAll['df'], questions_txt, cluster)

    context = {
        'cluster': cluster,
        'subcluster_id': 'a',
        'charts': charts,
        'group_size': len(df.index),#no of rows in df
        'survey_size': dic['orig_size'],
        'questions_strs': questions_strs,
        'about': about,
        'subcluster_values': list(clusters_dict.values()),
        'num_of_clusters': cluster.num_of_clusters,
        'compare': True,
    }
    return render(request, 'clusters/detail.html', context)

def increase_num_of_clusters(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    cluster.num_of_clusters += 1
    cluster.save()
    #clustering.increment_num_of_clusters()
    print "increased_num_of_clusters"
    return redirect('/clusters/'+cluster_id+'/stats')

def decrease_num_of_clusters(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    cluster.num_of_clusters -= 1
    cluster.save()
    print "decreased_num_of_clusters"
    return redirect('/clusters/'+cluster_id+'/stats')

def create_cluster(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ClusterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # redirect to a new URL:
            print 'sucess'
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        print "fail"
        form = ClusterForm()

    return render(request, 'clusters/form.html', {'form': form})

def survey_questions(request):
    #load csv
    df = utils.get_whole_survey()
    #load questionchoices txt
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt'))
    dic_source = rt.read(file2_)
    about = dic_source['about']
    questions_txt = dic_source['questions']
    file2_.close()

    context = {
        'questions': questions_txt.values(),
        'about': about,
    }
    return render(request, 'clusters/survey.html', context)

def see_question_answers(request, question):
    #load csv
    df = utils.get_whole_survey()
    #load questionchoices txt
    file2_ = open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt'))
    dic_source = rt.read(file2_)
    about = dic_source['about']
    questions_txt = dic_source['questions']
    file2_.close()

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

def get_charts(df, questions_txt, cluster, subcluster_id):
    charts = []

    questions_to_show = ['WARD', 'Q11', 'QGEN', 'QAGEBND', 'Q34', 'Q43', 'Q46', 'Q47']
    for question in questions_to_show:
        try:
            dic =  rc.get_data_for_pie_charts(df, questions_txt[question], cluster, subcluster_id)
        except KeyError:
            continue
        data = dic['data']
        question = dic['question']
        options={
            'title': question,
            'isStacked': 'percent',
        }
        charts.append(PieChart(SimpleDataSource(data=data), options=options))

    #Single code quesitions
    questions_to_show = ['QETH', 'Q35']

    for question in questions_to_show:
        try:
            dic =  rc.get_data_for_stacked_bar_charts(df, questions_txt[question], cluster, subcluster_id)
        except KeyError:
            continue
        data = dic['data']
        question = dic['question']
        options={
            'title': question,
            'isStacked': 'percent',
        }
        charts.append(StackedBarChart(SimpleDataSource(data=data), options=options))

    #multicode questions
    questions_to_show = ['Q5', 'Q26', 'Q29', 'Q39', 'Q45', 'Q50']
    for question in questions_to_show:
        try:
            dic =  rc.get_data_for_bar_charts(df, questions_txt[question], cluster, subcluster_id)
        except KeyError:
            continue
        data = dic['data']
        question = dic['question']
        options={
            'title': question,
        }
        charts.append(BarChart(SimpleDataSource(data=data), options=options))

    dic =  rc.get_data_for_column_chart(df, questions_txt['Q13'], cluster, subcluster_id)
    data = dic['data']
    question = dic['question']
    options={
        'title': question,
        'legend':{'position': 'bottom'},
    }
    charts.append(ColumnChart(SimpleDataSource(data=data), options=options))

    return charts

def get_charts_compare(df, dfAll, questions_txt, cluster):
    charts = []

    #Single code quesitions
    questions_to_show = ['WARD','Q11', 'QGEN', 'QAGEBND', 'QETH', 'Q34']

    for question in questions_to_show:
        dic =  rc2.get_data_for_stacked_bar_charts2(df, dfAll, questions_txt[question], cluster)
        data = dic['data']
        question = dic['question']
        options = {
            'title': question,
            'isStacked': 'percent',
        }
        charts.append(StackedBarChart(SimpleDataSource(data=data), options=options))

    """
    #Multi code questions
    questions_to_show = ['Q26,A']

    for question in questions_to_show:
        q = question.split(',')
        dic =  rc2.get_data_for_bar_charts_adapted2(df, dfAll, questions_txt[q[0]], q[1], cluster)
        data = dic['data']
        question = dic['question']
        options = {
            'title': question,
            'isStacked': 'percent',
        }
        charts.append(StackedBarChart(SimpleDataSource(data=data), options=options))
        """

    #multicode questions
    questions_to_show = ['Q5', 'Q26', 'Q29', 'Q39', 'Q50']
    for question in questions_to_show:
        dic =  rc2.get_data_for_bar_charts2(df, dfAll, questions_txt[question], cluster)
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
