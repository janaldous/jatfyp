import string
import sys
import collections

class Question(object):
    def __init__(self, question_no, question_short, question_long, choices):
        self.question_no = question_no#question_no = 'Q'+number
        self.question_short = question_short
        self.question = question_long#original form of question
        self.choices = choices

    def get_question_and_choices(self):
        output = {}
        return self.question, self.choices, self._get_formated_choices()

    def _get_formated_choices(self):
        output = ""
        for key in sorted(self.choices):
            output += "%s - %s<br>" % (key, self.choices[key])
        return output


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
            try:
                question_short = q[1]
            except IndexError:
                print 'IndexError at readtxt.read; question_no:' + question_no
            question_long = q[2][:-1]
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
            questions[question_no] = Question(question_no, question_short, question_long, choices)
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
