import re

class Question(object):

    def __init__(self, text):
        self.text = text
        self.answers = []


class Answer(object):
    def __init__(self, text, correct):
        self.text = text
        self.correct = correct


class ParseError(ValueError):
    pass


class PieceParser(object):
    """Parse a corpus file.

    A corpus file is comprised of a series of questions and answers,
    followed by a block of text. For example:

        Question: Why?
        A!: Because
        A: Dunno

        Text:

        I like stuff and things; they are interesting and fun and joyous.
        Oh, and badgers too.

    """

    def __init__(self, source):
        """Parse the file. Source can be any file-like object."""
        self.questions = []

        # Separate out the metadata lines from the body text
        meta_lines = []

        for line in source:
            if line.startswith("Text:"):
                self.text = "".join(source)
                break
            else:
                meta_lines.append(line)

        classified_lines = [self._classify(line) for line in meta_lines]

        # Our current parse context: useful for when we've just had a question,
        # so we're expecting either answers or a blank line to take us back to
        # normal
        context = []

        for (line_type, match) in classified_lines:
            if line_type == "blank":
                context = []
            elif (context, line_type) == ([], "title"):
                self.title = match.group(1)
            elif (context, line_type) == ([], "source"):
                self.source = match.group(1)
            elif (context, line_type) == ([], "url"):
                self.url = match.group(1)
            elif (context, line_type) == ([], "question"):
                self.questions.append(Question(match.group(1)))
                context.append("question")
            elif (context, line_type) == (["question"], "answer"):
                answer = Answer(match.group("text"),
                                match.group("correct") is not None)
                self.questions[-1].answers.append(answer)
            elif (context, line_type) == ([], "order"):
                self.order = int(match.group(1))
            elif (context, line_type) == ([], "author"):
                self.author = match.group(1)
            else:
                raise ParseError("Illegal %s line: %r" % (line_type, line))

    CLASSIFICATIONS = {
        "title": re.compile('^Title: (.*)$'),
        "source": re.compile('^Source: (.*)$'),
        "url": re.compile('^URL: (.*)$'),
        "question": re.compile('^Question: (.*)$'),
        "answer": re.compile('^A(?P<correct>!)?: (?P<text>.*)$'),
        "order": re.compile('^Order: (.*)$'),
        "author": re.compile('^Author: (.*)$'),
        "blank": re.compile('^\s+$'),
    }

    def _classify(self, line):
        for (key, matcher) in self.CLASSIFICATIONS.items():
            match = matcher.match(line)
            if match:
                return (key, match)
        else:
            raise ParseError("Unrecognised line: %r" % line)

