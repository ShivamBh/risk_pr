# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-15 08:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_profile_trial_sub'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='valid_till',
            field=models.DateField(null=True),
        ),
    ]
