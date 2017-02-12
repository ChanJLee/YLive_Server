from django.contrib import admin

# Register your models here.
# Create your models here.
from django.db import models


class CategoryModel(models.Model):
    name = models.CharField(max_length=20)
