# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-01 05:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20170628_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='sec_level',
            field=models.CharField(choices=[('Green', 'Green'), ('Yellow', 'Yellow'), ('Amber', 'Amber'), ('Red', 'Red')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='sec_rating',
            field=models.CharField(choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High'), ('Ex', 'Extreme')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='terror_rating',
            field=models.CharField(choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High'), ('Ex', 'Extreme')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='travel_rating',
            field=models.CharField(choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High'), ('Ex', 'Extreme')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='rating',
            field=models.CharField(choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High'), ('Ex', 'Extreme')], max_length=2, null=True),
        ),
    ]
