# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0006_auto_20160602_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='age',
            field=models.IntegerField(),
        ),
    ]
