from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db.models import CASCADE

from AnchorModel.models import Anchor
from CategoryModel.admin import CategoryModel


class RoomModel(models.Model):
    title = models.CharField(max_length=20)
    last = models.DateTimeField(auto_now_add=True)
    categoryId = models.ForeignKey(CategoryModel, on_delete=CASCADE)
    ownerId = models.ForeignKey(Anchor, default=-1, on_delete=CASCADE)
    count = models.IntegerField(default=0)