# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-30 18:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0003_person_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='userModifier',
        ),
    ]
