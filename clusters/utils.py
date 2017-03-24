import readtxt as rt

""" dictionary of ward id and name """
WARD = {}

def get_wards():
    """ follows singleton design pattern, loads from file only if WARD is empty """
    if WARD == False:
        with open(os.path.join(settings.BASE_DIR, 'clusters/RSQquestionchoices.txt')) as f:
            dic_source = rt.read(f)
            WARD = dic_source['questions']['WARD'].choices
    return WARD
