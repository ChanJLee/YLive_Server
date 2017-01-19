# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-17 13:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FollowModel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followmode',
            name='userId',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]