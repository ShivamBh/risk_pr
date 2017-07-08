# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlashMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_number', models.CharField(max_length=30)),
                ('from_number', models.CharField(max_length=30)),
                ('sms_sid', models.CharField(blank=True, default='', max_length=34)),
                ('account_sid', models.CharField(blank=True, default='', max_length=34)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, default='', max_length=20)),
            ],
        ),
    ]
