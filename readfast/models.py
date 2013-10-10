from django.db import models


class Piece(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)

    source_url = models.URLField(blank=True)
    source_title = models.CharField(max_length=200, blank=True)

    slug = models.SlugField(unique=True)

    text = models.TextField()

    # Default to a nice big number so new ones go on the end
    order = models.IntegerField(default=1000)

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

    def __unicode__(self):
        return self.text


class ComprehensionAnswer(models.Model):
    """
    An answer to a question about a piece.
    e.g. "Mazz."
    """
    question = models.ForeignKey('ComprehensionQuestion',
                                 related_name="answers")
    text = models.CharField(max_length=200)
    correct = models.BooleanField()

    def __unicode__(self):
        return u"%s (%s)" % (self.text, self.correct)
