import readtxt as rt
import os
from django.conf import settings
import pandas as pd
import numpy as np

import readcsv as rc

""" dictionary of ward id and name """
WARD = {}
NUM_OF_WARDS = 22
SURVEY16 = None
SURVEYTXT = None

def get_wards():
    """ follows singleton design pattern, loads from file only if WARD is empty """
    global WARD
    if bool(WARD) == False:
        with open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt')) as f:
            dic_source = rt.read(f)
            WARD = dic_source['questions']['WARD'].choices
        #print "utils called ------"
    return WARD

def get_whole_survey():
    global SURVEY16
    if SURVEY16 is None:
        with open(os.path.join(settings.BASE_DIR, 'clusters/spss.csv')) as f:
            SURVEY16 = pd.read_csv(f)
            #clean: #NULL! into np.nan
            SURVEY16 = SURVEY16.replace('#NULL!', np.nan)
        print "utils called ------"
    return SURVEY16

def get_questions_txt():
    global SURVEYTXT
    if SURVEYTXT is None:
        with open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt')) as f:
            SURVEYTXT = rt.read(f)
    return SURVEYTXT

def get_questions_only():
    global SURVEYTXT
    if SURVEYTXT is None:
        SURVEYTXT = get_questions_txt()
    return SURVEYTXT['questions']

def get_cluster_from_whole_survey(cluster):
    df = get_whole_survey()
    df_filtered = rc.filter_by_cluster_only(df, cluster)
    return df_filtered

def get_survey_num_of_rows():
    return SURVEY16.shape[0]

def get_dict_of_questions():
    d = get_questions_only()
    output = {}
    for key, value in d.items():
         question, choices, choices_str = d[key].get_question_and_choices()
         output[key] = {
            'question_no': key,
            'question_str': question,
            'choices': choices,
            'choices_str': choices_str,
        }
    return output
