# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-30 18:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_person_usercreator'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 5, 30, 18, 20, 55, 191267, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
