# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-28 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clusters', '0002_auto_20170125_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='num_of_clusters',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
