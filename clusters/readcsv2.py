#import csv
import pandas as pd

import utils
import readcsv as rc

import os
import operator
from django.conf import settings

from .models import Cluster

import string
import clustering

"""
    This class is to get data for subgroup comparison
"""

def get_data_for_group_compare(question, choice):
    """ outputs list for Group Compare view
        Group = model.Cluster
        Value = value of group filtered by question and choice
        output = [[Group, Value], ...,  ...]
    """

    df = utils.get_whole_survey()

    output = []

    #column names
    output.append(['Group', 'Orig Value', 'Percent', 'Diff from Avg'])

    """
    for each cluster
        v = get value(c)
        output.append(c, v)
    """
    #TODO need to implement general method to get cluster_all, not just from pk=3
    cluster_all = Cluster.objects.get(pk=3)
    value = df[question].value_counts()[int(choice)]
    average = float(value)/df.shape[0]

    cluster_models = Cluster.objects.all()
    for cluster in cluster_models:
        temp = rc.filter_by_cluster_only(df, cluster)
        try:
            value = temp[question].value_counts()[int(choice)]
            percent = float(value)/temp.shape[0]#percent
        except KeyError:
            value = 0
            percent = 0
        except IndexError:
            """ when value_counts only gives #NULL! """
            value = 0
            percent = 0
        diff_from_avg = percent-average
        output.append([cluster.name, value, percent, diff_from_avg])

    return output

def get_data_for_map4(df, question_base, choice):
    """
    outputs opposite of get_data_for_map2 (swapped columns) for column data chart format
    for views.json4
    """
    output = []
    cluster_rows = df
    output.append(["value", "Ward"])
    #for each ward get number of people who chose choice
    # cluster_rows.loc[cluster_rows['WARD'] == 2]['Q11'].value_counts()[1.0]
    # int(choice) == 1.0
    for i in range(1,22): #WARD IS STATIC
        ward_rows = cluster_rows.loc[cluster_rows['WARD'] == i]
        v_counts = ward_rows[question_base].value_counts()

        try:
            value = v_counts[int(choice)]
        except KeyError:
            value = 0
        except IndexError:
            value = 0

        ward = utils.get_wards()[str(i)]
        output.append([value, ward])

    return output

def get_data_for_map3(df, question_base):
    output = []
    cluster_rows = df
    output.append(["Max choice", "Ward"])
    #for each ward get number of people who chose choice
    # cluster_rows.loc[cluster_rows['WARD'] == 2]['Q11'].value_counts()[1.0]
    # int(choice) == 1.0
    for i in range(1,22): #WARD IS STATIC
        ward_rows = cluster_rows.loc[cluster_rows['WARD'] == i]
        value = int(ward_rows[question_base].value_counts().index[0])
        ward = str(i)
        output.append([value, ward])

    return output

def get_data_for_map2(df, question_base, choice):
    output = []
    cluster_rows = df
    output.append(["Population", "Ward"])
    #for each ward get number of people who chose choice
    # cluster_rows.loc[cluster_rows['WARD'] == 2]['Q11'].value_counts()[1.0]
    # int(choice) == 1.0
    for i in range(1,utils.NUM_OF_WARDS): #WARD IS STATIC
        ward_rows = cluster_rows.loc[cluster_rows['WARD'] == i]
        v_counts = ward_rows[question_base].value_counts()

        try:
            value = v_counts[int(choice)]
        except KeyError:
            value = 0
        except IndexError:
            value = 0
        ward = str(i)
        output.append([value, ward])

    return output

def get_data_for_map(df, question_obj):
    """ used by the map
        output sorted by value
        Ward is in int form
    """
    question_base = question_obj.question_no
    choices = question_obj.choices

    output = []
    v_counts = df[question_base].value_counts()

    output.append(["value", "Ward"])
    for i in range(1,utils.NUM_OF_WARDS):
        try:
            value = v_counts[i]
        except KeyError:
            value = 0
        output.append([value, i])

    return output

def get_data_for_mapv2(df, question_obj):
    """ used by Ward chart
        output sorted by value
        Ward is in String form
    """
    question_base = question_obj.question_no
    choices = question_obj.choices

    output = []
    v_counts = df[question_base].value_counts()

    output.append(["value", "Ward"])

    for i in range(1,utils.NUM_OF_WARDS):
        try:
            value = v_counts[i]
        except KeyError:
            value = 0
        ward = choices[str(int(i))]
        output.append([value, ward])

    return output

def get_data_for_stacked_bar_charts2(df, dfAll, question_obj):
    '''
        Creates data list in the form for stacked barcharts
        Choices are dependent on if choice exists in spss.csv
    '''
    question_base = question_obj.question_no
    choices = question_obj.choices

    v_counts = df[question_base].value_counts()

    indexes = ['Questions']
    for i in v_counts.index.tolist():
        indexes.append(str(int(i)))

    #get this cluster
    values = ['Cluster']
    for i in v_counts.values.tolist():
        values.append(i)

    #get subclusters
    valueslist = []
    for i in range(clustering.get_num_of_subclusters()):
        values2 = ['Cluster '+str(i)]
        dfclus = clustering.filter_by_subcluster(df, i)

        v_counts = dfclus[question_base].value_counts()
        for i in indexes[1:]:
            try:
                values2.append(v_counts[float(i)])
            except KeyError:
                values2.append(0)
        valueslist.append(values2)

    #get all pop
    valuesAll = ['All']
    v_countsAll = dfAll[question_base].value_counts()
    for i in indexes[1:]:
        valuesAll.append(v_countsAll[float(i)])

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    #change indexes from float to string description
    for idx,item in enumerate(indexes[1:]):
        try:
            c = choices[str(item)]
        except KeyError:
            c = item
            print 'key error AT readcsv.get_data; subquestion: %d' % (int(float(item)))
        indexes[idx] = c

    data = [indexes, values, valuesAll]
    for i in valueslist:
        data.append(i)

    return {'data':data, 'question':question_str}

def get_data_for_bar_charts2(df, dfAll, question_obj):
    '''
        Creates data lists in the form for bar charts
        Choices are dependent on whether it exists in XXXquestionchoices.txt
        and data is from spss.csv
    '''
    question_base = question_obj.question_no
    choices = question_obj.choices
    #ratio to make proportionate dfAll
    ratio = len(dfAll.index)/len(df.index)

    data = [['question', 'This cluster', 'Lambeth', 'question letter']]
    #append data to list
    for key in choices.keys():
        subquestion = question_base+key
        try:
            v_counts = df[subquestion].value_counts()
            v = v_counts[1]
        except KeyError:
            v = 0
        try:
            v_countsAll = dfAll[subquestion].value_counts()
            vAll = v_countsAll[1]/ratio
        except KeyError:
            vAll = 0
        choice_str = choices[key]
        data.append([choice_str, v, vAll, key])

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':data, 'question':question_str}

def get_data_for_column_chart2(df, question_obj):
    '''
        Creates data lists in the form for column charts
    '''
    data = [['question', 'Strongly Agree', 'Agree', 'Neither agree nor disagree', 'Disagree', 'Strongly disagree', 'Don\'t know']]
    choices = question_obj.choices
    for i in range(1,9):
        data_ = []
        subquestion = question_obj.question_no+'_R'+str(i)
        data_.append(choices[str(i)])
        values = df[subquestion].value_counts()
        for j in range(1,7):
            try:
                data_.append(values[j])
            except KeyError:
                data_.append(0)
                # 'key error at readcsv.get_data_for_column_chart; subquestion: %s' % subquestion
                continue
        data.append(data_)

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':data, 'question':question_str}
