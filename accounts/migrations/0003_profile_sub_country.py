# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 21:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20170628_2141'),
        ('accounts', '0002_auto_20170629_0253'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sub_country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.Country'),
        ),
    ]
