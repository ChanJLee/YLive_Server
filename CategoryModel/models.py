from django.db import models

from misc.base import DEFAULT_CHAR_LENGTH


class CategoryModel(models.Model):
    name = models.CharField(max_length=DEFAULT_CHAR_LENGTH)
