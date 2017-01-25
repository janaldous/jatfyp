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

#unused
def get_uc_list():
    uc_list = list(string.ascii_uppercase)
    iters = len(uc_list)
    for i in range(0,iters):
        uc_list.append('A'+uc_list[i])
    return uc_list

def get_data(df, question, question_obj):
    v_counts = df[question].value_counts()
    choices = question_obj.choices

    indexes = ['Question']
    for i in v_counts.index.tolist():
        try:
            c = choices[str(int(i))]
        except KeyError:
            c = str(int(i))
            print 'key error: %s' % (int(i))
        indexes.append(c)

    values = [question]
    for i in v_counts.values.tolist():
        values.append(i)

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':[indexes, values], 'question':question_str}

def get_data2(df, question_base, question_obj):
    choices = question_obj.choices

    data = {} #[['question', '#rows = 1']] #'#rows = 0']]
    #append data to list
    for l in get_uc_list():
        subquestion = question_base+l
        try:
            data[choices[l]] = df[subquestion].value_counts()[1]
            #data_.append(choices[l])
            #data_.append(df[subquestion].value_counts()[1])
            #data_.append(df[subquestion].value_counts()[0])
        except KeyError:
            break


    sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)

    data = [['question', '#rows = 1']]
    for d in sorted_data:
        data.append([d[0], d[1]])

    question_str = "(%s) %s" % (question_obj.question_no, question_obj.question)

    return {'data':data, 'question':question_str}

def get_data_for_column_chart(df):
    data = [['question', '1', '2', '3', '4', '5', '6']]


    for i in range(1,9):
        data_ = []
        question = 'Q13_R'+str(i)
        data_.append(question)
        values = df[question].value_counts()
        for j in range(1,7):
            data_.append(values[j])
        data.append(data_)

    return data

#filter rows, according to cluster factors
#http://stackoverflow.com/questions/11869910/pandas-filter-rows-of-dataframe-with-operator-chaining
