# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 20:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20170725_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('H', 'High Priority'), ('M', 'Medium Priority'), ('L', 'Low Priority')], default='M', max_length=1),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(help_text='Enter a due date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='notes',
            field=models.TextField(blank=True, help_text='Enter task notes', null=True),
        ),
    ]