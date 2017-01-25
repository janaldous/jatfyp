#import csv
import pandas as pd

import os
import operator
from django.conf import settings

import string

def start():
    df = pd.read_csv('spss.csv')
    print "adfadf"
    print get_data2(df, 'Q5')

def get_data(df, question_obj):
    '''
        Choices are dependent on if choice exists in spss.csv
    '''
    question_base = question_obj.question_no
    v_counts = df[question_base].value_counts()
    choices = question_obj.choices

    indexes = ['Question']
    for i in v_counts.index.tolist():
        try:
            c = choices[str(int(i))]
        except KeyError:
            c = str(int(i))
            print 'key error AT readcsv.get_data; subquestion: %s' % (int(i))
        indexes.append(c)

    values = [question_base]
    for i in v_counts.values.tolist():
        values.append(i)

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':[indexes, values], 'question':question_str}

def get_data2(df, question_obj):
    '''
        Choices are dependent on whether it exists in XXXquestionchoices.txt
        and data is from spss.csv
    '''
    question_base = question_obj.question_no
    choices = question_obj.choices

    data = {}
    #append data to list
    for key in choices.keys():
        subquestion = question_base+key
        try:
            choice_str = choices[key]
            data[choice_str] = df[subquestion].value_counts()[1]
        except KeyError:
            #print 'key error at readcsv.get_data2; subquestion: %s' % subquestion
            continue
        except IndexError:
            '''
                means that all rows = 0, no rows = 1
            '''
            data[choice_str] = 0
            continue

    #sort data fron greatest to least
    sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)

    #put sorted data into list
    data = [['question', '#rows = 1']]
    for d in sorted_data:
        data.append([d[0], d[1]])

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':data, 'question':question_str}

def get_data_for_column_chart(df, question_obj):
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

def filter_by_cluster(df, cluster):
    if cluster.factor1 != '-':
        df = df[(df.Q43 == float(cluster.factor1))]
    if cluster.factor3 != '-':
        df = df[(df.Q46 == float(cluster.factor3))]
    if cluster.factor4 != '-':
        df = df[(df.Q47 == float(cluster.factor4))]
    if cluster.factor5 != '-':
        df = df[(df.Q35 == float(cluster.factor5))]
    return df

#filter rows, according to cluster factors
#http://stackoverflow.com/questions/11869910/pandas-filter-rows-of-dataframe-with-operator-chaining
