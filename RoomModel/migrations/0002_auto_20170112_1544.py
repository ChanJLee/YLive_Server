# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-12 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoomModel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roommodel',
            name='last',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]