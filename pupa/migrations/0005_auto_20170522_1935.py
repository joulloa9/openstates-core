# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-22 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pupa', '0004_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identifier',
            name='identifier',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='identifier',
            name='object_id',
            field=models.CharField(max_length=300),
        ),
    ]
