# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-25 07:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20170915_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='valid_till',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]