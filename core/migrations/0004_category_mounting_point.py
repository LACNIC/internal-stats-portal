# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-07 19:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170307_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='mounting_point',
            field=models.CharField(default='N/A', max_length=20),
        ),
    ]
