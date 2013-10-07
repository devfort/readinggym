from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    
    def __unicode__(self):
      return self.name
