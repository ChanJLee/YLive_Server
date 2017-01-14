from __future__ import unicode_literals

from django.db import models

# Create your models here.
from AnchorModel.models import Anchor
from CategoryModel.models import CategoryModel


class RoomModel(models.Model):
    title = models.CharField(max_length=20)
    last = models.DateTimeField(auto_now_add=True)
    houseCount = models.IntegerField(default=0)
    categoryId = models.ForeignKey(CategoryModel)
    ownerId = models.ForeignKey(Anchor, default=-1)
    followCount = models.IntegerField(default=0)
