from __future__ import unicode_literals

# Create your models here.
from django.db import models
from django.db.models import Model


class CategoryModel(models.Model):
    name = models.CharField(max_length=20)
