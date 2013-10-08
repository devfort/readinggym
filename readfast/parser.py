import re

class Question(object): pass


class Answer(object): pass


class PieceParser(object):

    TITLE = re.compile('^Title: (.*)$')
    QUESTION = re.compile('^Question: (.*)$')
    ANSWER = re.compile('^A(?P<correct>!)?: (?P<text>.*)$')

    TEXT = re.compile('^Text:')

    def __init__(self, source):
        self.questions = []

        while True:
            try:
                line = source.next()
            except StopIteration:
                break

            if self.TEXT.match(line):
                # We're done here: anything else in the source is body text
                self.text = "".join(source)
                break

            title_match = self.TITLE.match(line)
            if title_match:
                self.title = title_match.group(1)
                continue

            question_match = self.QUESTION.match(line)
            if question_match:
                q = Question()
                self.questions.append(q)
                q.text = question_match.group(1)
                q.answers = []
                while True:
                    answer_match = self.ANSWER.match(source.next())
                    if answer_match:
                        a = Answer()
                        a.text = answer_match.group("text")
                        a.correct = (answer_match.group("correct") is not None)
                        q.answers.append(a)
                    else:
                        break
