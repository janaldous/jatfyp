import string

class Question(object):
    def __init__(self, question_no, question, choices):
            self.question_no = question_no
            self.question = question
            self.choices = choices

def read(file_):
    questions = {}
    with open(file_.name) as f:
        #get first '$'
        line=f.readline()
        while True:
            line=f.readline()
            if not line:
                break
            #get q_no and question
            q = line.split(',')
            question_no = q[0]
            question = q[1][:-1]
            #get choices
            choices = {}
            while True:
                line=f.readline()
                if not line or line[:1] == '$':
                    break
                l = line.split(',')
                choices[l[0]] = l[1][:-1]
            questions[question_no] = Question(question_no, question, choices)
        return questions


def find_and_replace():
    newf = open('newfile.txt', 'w')
    with open('ResidentialSurveyQuestions.txt', 'rw') as f:
        for line in f.readlines():
            line = string.replace(line,'\r','\n')
            newf.write(line)
    newf.close()
