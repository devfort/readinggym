from StringIO import StringIO

from django.test import TestCase

from readfast.parser import PieceParser

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
