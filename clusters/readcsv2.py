import pandas as pd

import utils
import readcsv as rc

import os
import operator
from django.conf import settings

from .models import Cluster

import string
import clustering

""" This module is to get data for subgroup comparison
"""

def get_data_for_bar_charts(df, question_obj):
    """ Creates data lists in the form for bar charts
        Choices are dependent on whether it exists in XXXquestionchoices.txt
        and data is from spss.csv
    """
    question_base = question_obj.question_no
    choices = question_obj.choices

    data = [[question_base, '#rows = 1', 'question_letter']]
    #append data to list
    for key in choices.keys():
        subquestion = question_base+key

        try:
            question_text = choices[key]
            value = df[subquestion].value_counts()[1]
        except KeyError:
            #print 'key error at readcsv.get_data2; subquestion: %s' % subquestion
            continue
        except IndexError:
            #means that all rows = 0, no rows = 1
            value = 0
            continue
        data.append([question_text, value, key])

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':data, 'question':question_str}

def get_data_for_group_compare(question, choice):
    """ outputs list for Group Compare view
        Group = model.Cluster
        Value = value of group filtered by question and choice
        output = [[Group, Value], ...,  ...]
    """
    output = []

    #column names
    output.append(['Group', 'Orig Value', 'Percent', '% Diff from Avg'])

    if question == '0' and choice == '0':

        cluster_models = Cluster.objects.all()
        for cluster in cluster_models:
            output.append([cluster.name, 0, 0, 0])

        return output

    df = utils.get_whole_survey()


    """
    for each cluster
        v = get value(c)
        output.append(c, v)
    """
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
        diff_from_avg = (percent-average)*100
        output.append([cluster.name, value, percent, diff_from_avg])

    return output

def get_data_for_map4(df, question_base, choice):
    """ outputs opposite of get_data_for_map2 (swapped columns) for column data chart format
        for views.json4
    """
    output = []
    cluster_rows = df
    output.append(["# of residents", "Ward"])

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

    output.append(["# of Residents", "Ward"])
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

    output.append(["# of Residents", "Ward"])

    for i in range(1,utils.NUM_OF_WARDS):
        try:
            value = v_counts[i]
        except KeyError:
            value = 0
        ward = choices[str(int(i))]
        output.append([value, ward])

    return output

def get_data_for_stacked_bar_charts2(df, dfAll, question_obj, cluster):
    """ Creates data list in the form for stacked barcharts
        Choices are dependent on if choice exists in spss.csv
    """
    question_base = question_obj.question_no
    choices = question_obj.choices

    v_counts = df[question_base].value_counts()

    indexes = [question_base]
    indexes_int = ['choice_id']

    for i in v_counts.index.tolist():
        indexes.append(str(int(i)))


    #get this cluster
    values = ['This group']
    for i in v_counts.values.tolist():
        values.append(i)

    #get subclusters
    valueslist = []
    subclusters_dict = clustering.get_subclusters(cluster, df)
    for i in range(len(subclusters_dict)):
        values2 = ['Cluster '+str(i)]
        dfclus = subclusters_dict[i]

        v_counts = dfclus[question_base].value_counts()
        for j in indexes[1:]:
            try:
                values2.append(v_counts[float(j)])
            except KeyError:
                values2.append(0)
        #append subcluster id to last column in this row
        values2.append(str(cluster.id)+"/"+str(i))
        valueslist.append(values2)

    #get all pop
    valuesAll = ['All']
    v_countsAll = dfAll[question_base].value_counts()
    for i in indexes[1:]:
        valuesAll.append(v_countsAll[float(i)])


    #change indexes from float to string description
    for idx,item in enumerate(indexes[1:]):
        try:
            c = choices[str(item)]
        except KeyError:
            c = item
            print 'key error AT readcsv.get_data; subquestion: %d' % (int(float(item)))
        indexes[idx+1] = c
        indexes_int.append(int(item))

    data = [indexes, values, valuesAll]
    for i in valueslist:
        data.append(i)
    data.append(indexes_int)

    #append subcluster id to last column in row
    indexes.append('subcluster_id')
    values.append(str(cluster.id)+'/a')#all of this cluster
    valuesAll.append('3/a')#all of all cluster
    indexes_int.append('NA')#not applicable

    #title for chart
    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':data, 'question':question_str}

def get_data_for_bar_charts_adapted2(df, dfAll, question_obj, letter, cluster):
    """ adapted for multicode quesitons
        @param letter is question letter
        Creates data lists in the form for bar charts
        Choices are dependent on whether it exists in XXXquestionchoices.txt
        and data is from spss.csv
    """
    question_base = question_obj.question_no+letter

    v_counts = df[question_base].value_counts()

    indexes = [question_base]
    indexes_int = ['choice_id']

    for i in v_counts.index.tolist():
        if not pd.isnull(i):
            indexes.append(str(int(float(i))))

    #get this group
    values = ['This group'] + v_counts.values.tolist()

    #get subclusters
    valueslist = []
    subclusters_dict = clustering.get_subclusters(cluster, df)
    for i in range(len(subclusters_dict)):
        values2 = ['Cluster '+str(i)]
        dfclus = subclusters_dict[i]
        try:
            v_counts = dfclus[question_base].value_counts()

            for j in indexes[1:]:
                try:
                    values2.append(v_counts[int(j)])
                except KeyError:
                    values2.append(0)
                except IndexError:
                    values2.append(0)
        except KeyError:
            for j in indexes[1:]:
                values2.append(0)

        #append subcluster id to last column in this row
        values2.append(str(cluster.id)+"/"+str(i))
        valueslist.append(values2)

    #get all pop
    valuesAll = ['All']
    v_countsAll = dfAll[question_base].value_counts()

    for i in indexes[1:]:
        try:
            valuesAll.append(v_countsAll[int(i)])
        except KeyError:
            valuesAll.append(0)

    q13 = ['Strongly Agree', 'Agree', 'Neither agree nor disagree', 'Disagree', 'Strongly disagree', 'Don\'t know']

    #change indexes from float to string description
    for idx,item in enumerate(indexes[1:]):
        c = item
        indexes[idx+1] = c
        if question_base.startswith('Q13'):
            indexes[idx+1] = q13[int(c)-1]
        indexes_int.append(int(item))

    data = [indexes, values, valuesAll]
    for i in valueslist:
        data.append(i)
    data.append(indexes_int)

    #append subcluster id to last column in row
    indexes.append('subcluster_id')
    values.append(str(cluster.id)+'/a')#all of this cluster
    valuesAll.append('3/a')#all of all cluster
    indexes_int.append('NA')#not applicable

    #title for chart
    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':data, 'question':question_str}

def get_data_for_bar_charts2(df, dfAll, question_obj, cluster):
    """ Creates data lists in the form for bar charts
        Choices are dependent on whether it exists in XXXquestionchoices.txt
        and data is from spss.csv
    """
    question_base = question_obj.question_no
    choices = question_obj.choices
    #ratio to make proportionate dfAll
    ratio = len(dfAll.index)/len(df.index)

    data = [[question_base, 'This cluster', 'Lambeth', 'question letter']]
    #append data to list
    for key in choices.keys():
        subquestion = question_base+key
        try:
            v_counts = df[subquestion].value_counts()
            v = v_counts[1]
        except KeyError:
            v = 0
        except IndexError:
            v = 0
        try:
            v_countsAll = dfAll[subquestion].value_counts()
            vAll = v_countsAll[1]/ratio
        except KeyError:
            vAll = 0
        except IndexError:
            v = 0
        choice_str = choices[key]
        data.append([choice_str, v, vAll, key])

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':data, 'question':question_str}

def get_data_for_column_chart2(df, question_obj):
    """ Creates data lists in the form for column charts
    """
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
