# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 08:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0009_auto_20170703_0011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='rating',
            new_name='political_rating',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='sec_rating',
            new_name='security_rating',
        ),
    ]