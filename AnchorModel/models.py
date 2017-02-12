# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import CASCADE


class Anchor(models.Model):
    user = models.ForeignKey(User, default=-1, on_delete=CASCADE, related_name=u'anchor_user')
    followers = models.ManyToManyField(
        User,
        through="UserToAnchorRelationship",
        through_fields=('anchor', 'audience',),
    )


class UserToAnchorRelationship(models.Model):
    audience = models.ForeignKey(User, on_delete=CASCADE)
    anchor = models.ForeignKey(Anchor, on_delete=CASCADE)
