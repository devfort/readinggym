from django.db import models


class Piece(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()

    def __unicode__(self):
        return self.name


class ComprehensionQuestion(models.Model):
    """
    A question about a piece.
    e.g. "Who ate the otter?"
    """
    piece = models.ForeignKey('Piece',
                              related_name="questions")
    text = models.CharField(max_length=200)


class ComprehensionAnswer(models.Model):
    """
    An answer to a question about a piece.
    e.g. "Mazz."
    """
    question = models.ForeignKey('ComprehensionQuestion',
                                 related_name="answers")
