# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 00:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='done',
            field=models.BooleanField(default=None),
        ),
    ]
