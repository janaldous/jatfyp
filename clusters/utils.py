import readtxt as rt
import os
from django.conf import settings
import pandas as pd

""" dictionary of ward id and name """
WARD = {}
NUM_OF_WARDS = 22
SURVEY16 = None

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
        print "utils called ------"
    return SURVEY16
