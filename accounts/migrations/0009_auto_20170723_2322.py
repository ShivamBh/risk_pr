# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-23 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20170722_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]
