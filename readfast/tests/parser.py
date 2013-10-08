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
