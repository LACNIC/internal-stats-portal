# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-30 19:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20170314_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='fecha de creaci\xf3n'),
        ),
    ]
