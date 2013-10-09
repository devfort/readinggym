from StringIO import StringIO

from django.test import TestCase

from readfast.parser import PieceParser, ParseError

class ParserTest(TestCase):

    def test_extracts_title(self):
        source = StringIO("""
Title: A Tale Of Otters

Text:
Something something otters.
""")
        p = PieceParser(source)
        self.assertEqual(p.title, "A Tale Of Otters")

    def test_extracts_text(self):
        source = StringIO("""
Title: A Tale Of Otters

Text:
Something something otters.
Something something else.
""")
        p = PieceParser(source)
        self.assertEqual(
            p.text,
            "Something something otters.\nSomething something else.\n"
        )

    def test_extracts_source_info(self):
        source = StringIO("""
Source: Otters and stuff, by me
URL: http://example.com

Text:
Something something otters.
        """)

        p = PieceParser(source)
        self.assertEqual(p.source, "Otters and stuff, by me")
        self.assertEqual(p.url, "http://example.com")

    def test_extracts_question_and_answer(self):
        source = StringIO("""
Question: What are otters?
A!: Delicious

Text:
Something something otters.
        """)

        p = PieceParser(source)
        self.assertEqual(len(p.questions), 1)
        self.assertEqual(p.questions[0].text, "What are otters?")
        self.assertEqual(len(p.questions[0].answers), 1)
        self.assertEqual(p.questions[0].answers[0].text, "Delicious")
        self.assertTrue(p.questions[0].answers[0].correct)

    def test_extracts_multiple_questions(self):
        source = StringIO("""
Question: What are otters?
A: Alright
A!: Delicious

Question: How do you feel?
A!: I do not understand the question, mother
A: Reasonable
        """)

        p = PieceParser(source)
        self.assertEqual(len(p.questions), 2)
        self.assertEqual([len(q.answers) for q in p.questions], [2, 2])
        self.assertEqual([q.correct for q in p.questions[0].answers],
                         [False, True])
        self.assertEqual([q.correct for q in p.questions[1].answers],
                         [True, False])

    def test_fails_on_unexpected_line(self):
        source = StringIO("""
Question: What are otters?
A: Alright
A!: Delicious
I was the turkey all along!
        """)

        self.assertRaises(ParseError, PieceParser, source)

    def test_fails_on_unexpected_meta_line(self):
        source = StringIO("""
Question: What are otters?
A: Alright
A!: Delicious
Title: Things!
        """)

        self.assertRaises(ParseError, PieceParser, source)
