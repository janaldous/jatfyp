#import csv
import pandas as pd

import os
import operator
from django.conf import settings

import string

def get_data_for_map3(df, question_base):
    output = []
    cluster_rows = df
    output.append(["Max choice", "Ward"])
    #for each ward get number of people who chose choice
    #print cluster_rows.loc[cluster_rows['WARD'] == 2]['Q11'].value_counts()[1.0]
    #print int(choice) == 1.0
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
    #print cluster_rows.loc[cluster_rows['WARD'] == 2]['Q11'].value_counts()[1.0]
    #print int(choice) == 1.0
    for i in range(1,22): #WARD IS STATIC
        ward_rows = cluster_rows.loc[cluster_rows['WARD'] == i]
        v_counts = ward_rows[question_base].value_counts()

        try:
            value = v_counts[int(choice)]
        except KeyError:
            value = 0
        ward = str(i)
        output.append([value, ward])

    return output

def get_data_for_map(df, question_base):
    output = []
    v_counts = df[question_base].value_counts()

    output.append(["value", "Ward"])
    for i in range(1,22):
        try:
            value = v_counts[i]
        except KeyError:
            value = 0
        ward = str(i)
        output.append([value, ward])

    return output

def get_data_for_stacked_bar_charts2(df, dfAll, question_obj):
    '''
        Creates data list in the form for stacked barcharts
        Choices are dependent on if choice exists in spss.csv
    '''
    question_base = question_obj.question_no
    v_counts = df[question_base].value_counts()
    choices = question_obj.choices

    indexes = ['Cluster']
    for i in v_counts.index.tolist():
        try:
            c = choices[str(int(i))]
        except KeyError:
            c = str(int(i))
            print 'key error AT readcsv.get_data; subquestion: %s' % (int(i))
        indexes.append(c)

    values = ['This cluster']
    for i in v_counts.values.tolist():
        values.append(i)

    valuesAll = ['All']
    v_countsAll = dfAll[question_base].value_counts()
    for i in v_counts.index.tolist():
        valuesAll.append(v_countsAll[i])

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':[indexes, values, valuesAll], 'question':question_str}

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

    data = [['question', 'This cluster', 'Lambeth']]
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
        data.append([choice_str, v, vAll])

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
                #print 'key error at readcsv.get_data_for_column_chart; subquestion: %s' % subquestion
                continue
        data.append(data_)

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':data, 'question':question_str}
