#import csv
import pandas as pd

import os
from django.conf import settings

import string

def start():
    df = pd.read_csv('spss.csv')
    print "adfadf"
    print get_data2(df, 'Q5')

def get_uc_list():
    uc_list = list(string.ascii_uppercase)
    for l in uc_list:
        uc_list.append('A'+l)

def get_data(df, question):
    v_counts = df[question].value_counts()

    indexes = ['Question']
    for i in v_counts.index.tolist():
        indexes.append(str(i))

    values = [question]
    for i in v_counts.values.tolist():
        values.append(i)

    return [indexes, values]

def get_data2(df, question_base):
    uc_list = list(string.ascii_uppercase)

    data = [['question', '#rows = 1']] #'#rows = 0']]

    for l in uc_list:
        data_ = []
        subquestion = question_base+l
        data_.append(subquestion)
        try:
            data_.append(df[subquestion].value_counts()[1])
            #data_.append(df[subquestion].value_counts()[0])
        except KeyError:
            break
        data.append(data_)

    return data

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
