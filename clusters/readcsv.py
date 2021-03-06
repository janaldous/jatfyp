import pandas as pd

import os
import operator
from django.conf import settings
from models import Cluster
import string

def get_data_for_question(df, question_obj, letter=None):
    question_base = question_obj.question_no
    if letter != None:
        question_base = question_base + letter
    v_counts = df[question_base].value_counts()
    choices = question_obj.choices
    indexes = ['Group']
    index_ = []

    iterate = question_obj.choices
    if question_obj.choices == {} or letter != None:
        iterate = v_counts.index.tolist()
    for i in iterate:
        index_.append(i)
        try:
            c = choices[str(int(i))]
        except KeyError:
            c = str(int(i))
            #print 'key error AT readcsv.get_data_for_question; subquestion: %s' % (int(i))
        except ValueError:
            c = choices[str(i)]
        indexes.append(c)

    data = [indexes]

    for cluster in Cluster.objects.all():
        df2 = filter_by_cluster(df, cluster)['df']
        v_counts = df2[question_base].value_counts()
        values = [cluster.name]
        for i in index_:
            try:
                values.append(v_counts[int(i)])
            except KeyError:
                values.append(0)
            except IndexError:
                values.append(0)
        data.append(values)

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':data, 'question':question_str}

def get_data_for_pie_charts(df, question_obj, cluster, subcluster_id):
    """
        Creates data list in the form for stacked barcharts
        Choices are dependent on if choice exists in spss.csv
    """
    question_base = question_obj.question_no
    try:
        v_counts = df[question_base].value_counts()
    except KeyError:
        #question does not exist in df
        raise
    choices = question_obj.choices

    data = [['Ward', 'Value', 'Ward id', 'subcluster_id']]

    indexes = [question_base]

    #list in order of index
    l = v_counts.index.tolist()

    #values = ['Value']
    #ward id
    #ward_ids = ['Ward id']
    for i in l:
        try:
            c = choices[str(int(float(i)))]
        except KeyError:
            c = str(int(i))
            print 'key error AT readcsv.get_data; subquestion: %s' % (int(i))
        #indexes.append(c)
        #values.append(v_counts[i])
        #ward_ids.append()
        data.append([c, v_counts[i], int(float(i)), str(cluster.id)+"/"+subcluster_id])

    #data = [indexes, values, ward_ids]

    #print data

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':data, 'question':question_str}

def get_data_for_stacked_bar_charts(df, question_obj, cluster, subcluster_id):
    """
        Creates data list in the form for stacked barcharts
        Choices are dependent on if choice exists in spss.csv
    """
    question_base = question_obj.question_no
    try:
        v_counts = df[question_base].value_counts()
    except KeyError:
        raise
    choices = question_obj.choices

    indexes = [question_base]

    #list in order of index
    l = v_counts.index.tolist()
    #remove #NULL! from l
    if '#NULL!' in l:
        l.remove('#NULL!')

    values = ['Value']
    #ward id
    ward_ids = ['choice_id']
    for idx, i in enumerate(l):
        i = int(float(i))
        try:
            c = choices[str(int(i))]
        except KeyError:
            c = str(int(i))
            print 'key error AT readcsv.get_data; quetstion %s, subquestion: %s' % (question_base, int(i))
        except ValueError:
            """ means i = #NULL """
            print 'VALUE error AT readcsv.get_data; quetstion %s, subquestion: %s' % (question_base, i)
            c = choices[str(int(i))]

        indexes.append(c)
        try:
            values.append(v_counts[i])
        except IndexError:
            values.append(0)
        ward_ids.append(i)

    #append cluster/subcluster str as last column
    indexes.append('subcluster_id')
    values.append(str(cluster.id)+'/'+subcluster_id)#all of this cluster
    ward_ids.append('NA')#not applicable

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':[indexes, values, ward_ids], 'question':question_str}

def get_data_for_bar_charts(df, question_obj, cluster, subcluster_id):
    """Creates data lists in the form for bar charts
        Choices are dependent on whether it exists in XXXquestionchoices.txt
        and data is from spss.csv
    """
    question_base = question_obj.question_no
    choices = question_obj.choices

    data = [[question_base, '# of residents', 'question_letter', 'subcluster_id']]
    #append data to list
    for key in choices.keys():
        subquestion = question_base+key

        try:
            question_text = choices[key]
            value = df[subquestion].value_counts()[1]
        except KeyError:
            #print 'key error at readcsv.get_data2; subquestion: %s' % subquestion
            raise
        except IndexError:
            '''
                means that all rows = 0, no rows = 1
            '''
            value = 0
            continue
        data.append([question_text, value, key, str(cluster.id)+'/'+subcluster_id])

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':data, 'question':question_str}

def get_data_for_column_chart(df, question_obj, cluster, subcluster_id):
    """
        Creates data lists in the form for column charts
    """
    data = [['question', 'Strongly Agree', 'Agree', 'Neither agree nor disagree', 'Disagree', 'Strongly disagree', 'Don\'t know', 'subcluster_id']]
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
                #print 'key error at readcsv.get_data_for_column_chart; subquestion: %s' % subquestion
                continue
        data_.append(str(cluster.id)+'/'+subcluster_id)
        data.append(data_)

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':data, 'question':question_str}

def filter_by_cluster(df3, cluster):
    """ DOES NOT INCLUDE FACTOR2 YET """
    orig_size = len(df3.index)
    if cluster.factor1 != '-':
        df3 = df3[(df3.Q43 == float(cluster.factor1))]
    if cluster.factor2 != '-':
        question = 'Q45'+cluster.factor2
        df3 = df3[(df3[question] == 1.0)]
    if cluster.factor3 != '-':
        df3 = df3[(df3.Q46 == float(cluster.factor3))]
    if cluster.factor4 != '-':
        df3 = df3[(df3.Q47 == float(cluster.factor4))]
    if cluster.factor5 != '-':
        df3 = df3[(df3.Q35 == float(cluster.factor5))]
    return {'orig_size': orig_size, 'df': df3}

def filter_by_cluster_only(df3, cluster):
    """ DOES NOT INCLUDE FACTOR2 YET """
    orig_size = len(df3.index)
    if cluster.factor1 != '-':
        df3 = df3[(df3.Q43 == float(cluster.factor1))]
    if cluster.factor2 != '-':
        question = 'Q45'+cluster.factor2
        df3 = df3[(df3[question] == 1.0)]
    if cluster.factor3 != '-':
        df3 = df3[(df3.Q46 == float(cluster.factor3))]
    if cluster.factor4 != '-':
        df3 = df3[(df3.Q47 == float(cluster.factor4))]
    if cluster.factor5 != '-':
        df3 = df3[(df3.Q35 == float(cluster.factor5))]
    return df3
