import string
import sys

class Question(object):
    def __init__(self, question_no, question, choices):
        #question_no = 'Q'+number
        self.question_no = question_no
        self.question = question
        self.choices = choices

def read(file_):
    source = {}
    with open(file_.name) as f:
        #get about sources
        source['about'] = f.readline()
        #get first '$'
        line=f.readline()
        questions = {}
        while True:
            line=f.readline()
            if not line:
                break
            #get q_no and question
            q = line.split('|')
            question_no = q[0]
            question = q[1][:-1]
            #get type of coding ie MULTICODE, SINGLE
            code = f.readline()
            #get choices
            choices = {}
            while True:
                line=f.readline()
                if not line or line[:1] == '$':
                    break
                l = line.split(';')
                choices[l[0]] = l[1][:-1]
            questions[question_no] = Question(question_no, question, choices)
        source['questions'] = questions
        return source

def find_and_replace():
    newf = open('RSQquestionchoices.txt', 'w')
    with open('ResidentialSurveyQuestions.txt', 'rw') as f:
        for line in f.readlines():
            line = string.replace(line,'\r','\n')
            newf.write(line)
    newf.close()
    print 'found \ r and replaced by \ n'

if __name__ == "__main__":
    if sys.argv[1] == 'replace':
        find_and_replace()
