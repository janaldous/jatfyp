import string

class Question(object):
    def __init__(self, question_no, question, choices):
            self.question_no = question_no
            self.question = question
            self.choices = choices

def read():
    questions = []
    with open('newfile.txt') as f:
        #get first '$'
        line=f.readline()
        while True:
            line=f.readline()
            if not line:
                break
            #get q_no and question
            q = line.split(',')
            question_no = q[0]
            question = q[1]
            print question_no
            print question
            #get choices
            choices = {}
            while True:
                line=f.readline()
                if not line or line[:1] == '$':
                    break
                l = line.split(',')
                choices[l[0]] = l[1]
            print choices
            questions.append(Question(question_no, question, choices))
        return questions

read();

def rewrite():
    newf = open('newfile.txt', 'w')
    with open('ResidentialSurveyQuestions.txt', 'rw') as f:
        for line in f.readlines():
            line = string.replace(line,'\r','\n')
            newf.write(line)
    newf.close()
