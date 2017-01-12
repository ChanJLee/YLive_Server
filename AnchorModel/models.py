from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Anchor(models.Model):
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=11)
    age = models.IntegerField()
    email = models.CharField(max_length=30)
    signUpDate = models.DateField(auto_now_add=True)