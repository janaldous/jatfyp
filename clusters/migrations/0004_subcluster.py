# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-31 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clusters', '0003_cluster_num_of_clusters'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subcluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=8)),
                ('group', models.IntegerField(max_length=3)),
                ('subcluster', models.IntegerField(max_length=3)),
            ],
        ),
    ]
