# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-29 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('santa', '0004_auto_20180423_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='santa_version',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
