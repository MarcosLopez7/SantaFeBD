# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-05 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0007_auto_20160602_0135'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='person',
            name='age',
            field=models.IntegerField(max_length=2),
        ),
    ]
