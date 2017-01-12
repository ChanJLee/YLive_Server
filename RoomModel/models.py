from __future__ import unicode_literals

from django.db import models

# Create your models here.
class RoomModel(models.Model):
    title = models.CharField(max_length=20)
    last = models.DateTimeField(auto_now_add=True)
    houseCount = models.IntegerField(default=0)
    categoryId = models.IntegerField(default=-1)
    ownerId = models.IntegerField(default=-1)