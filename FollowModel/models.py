from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Model

from AnchorModel.models import Anchor
from CategoryModel.models import CategoryModel
from RoomModel.models import RoomModel

class FollowMode(models.Model):
    roomId = models.ForeignKey(RoomModel, default=-1)
    anchorId = models.ForeignKey(Anchor, default=-1)
    categoryId = models.ForeignKey(CategoryModel, default=-1)
    userId = models.ForeignKey(User, default=-1)
