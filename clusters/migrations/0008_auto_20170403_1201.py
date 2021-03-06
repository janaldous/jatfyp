# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-03 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clusters', '0007_auto_20170331_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cluster',
            name='factor1',
            field=models.CharField(choices=[('1', 'Has disability'), ('2', 'Has long term illness'), ('3', 'Has both disability and illness'), ('4', 'None'), ('-', 'Any of the above')], max_length=2),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='factor2',
            field=models.CharField(choices=[('A', 'Pension from a former employer'), ('B', 'State pension'), ('C', 'Child benefit'), ('D', 'Income support or Job seekers allowance'), ('E', 'Housing benefit'), ('F', 'Council tax benefit'), ('G', 'Any other state benefits'), ('-', 'Any of the above')], max_length=2),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='factor3',
            field=models.CharField(choices=[('1', 'Employee in full-time job'), ('2', 'Employee in part-time job'), ('3', 'Self employed full-time'), ('4', 'Self employed part-time'), ('5', 'On government supported training programme'), ('6', 'Full-time education at school, college or university'), ('7', 'Unemployed and available for work'), ('8', 'Permanently sick/disabled'), ('9', 'Wholly retired from work'), ('10', 'Looking after the home'), ('95', 'Doing something else'), ('98', 'Refused'), ('97', 'Dont know'), ('-', 'Any of the above')], max_length=2),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='factor4',
            field=models.CharField(choices=[('1', 'Yes I am paid the London Living Wage or higher amount'), ('2', 'I am paid less than the London Living Wage'), ('3', 'Dont know'), ('4', 'Prefer not to say'), ('-', 'Any of the above')], max_length=2),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='factor5',
            field=models.CharField(choices=[('1', 'Owner occupier - Lambeth leaseholder'), ('2', 'Owner occupier - private'), ('3', 'Rented from Housing Association'), ('4', 'Rengint from Lambeth Council'), ('5', 'Rent from private landlord'), ('6', 'Shared ownership'), ('7', 'A residential home'), ('95', 'Other'), ('98', 'Refused'), ('-', 'Any of the above')], max_length=2),
        ),
    ]
