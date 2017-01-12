from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Program:
    anchorId = models.IntegerField()
    title = models.CharField(max_length=30)
    category = models.IntegerField()
    audienceNum = models.IntegerField()
    last = models.DateField()
    coverImage = models.CharField(max_length=50)