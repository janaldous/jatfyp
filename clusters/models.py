from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Cluster(models.Model):
    #Q43
    DISABILITY = (
        ('1', 'Has disability'),
        ('2', 'Has long term illness'),
        ('3', 'Has both disability and illness'),
        ('4', 'None'),
        ('-', 'Any of the above'),
    )
    #Q45
    BENEFITS = (
        ('A', 'Pension from a former employer'),
        ('B', 'State pension'),
        ('C', 'Child benefit'),
        ('D', 'Income support or Job seekers allowance'),
        ('E', 'Housing benefit'),
        ('F', 'Council tax benefit'),
        ('G', 'Any other state benefits'),
        ('-', 'Any of the above'),
    )
    #Q46
    ACTIVITY = (
        ('1', 'Employee in full-time job'),
        ('2', 'Employee in part-time job'),
        ('3', 'Self employed full-time'),
        ('4', 'Self employed part-time'),
        ('5', 'On government supported training programme'),
        ('6', 'Full-time education at school, college or university'),
        ('7', 'Unemployed and available for work'),
        ('8', 'Permanently sick/disabled'),
        ('9', 'Wholly retired from work'),
        ('10', 'Looking after the home'),
        ('95', 'Doing something else'),
        ('98', 'Refused'),
        ('97', 'Dont know'),
        ('-', 'Any of the above'),
    )
    #Q47
    LLW = (
        ('1', 'Yes I am paid the London Living Wage or higher amount'),
        ('2', 'I am paid less than the London Living Wage'),
        ('3', 'Dont know'),
        ('4', 'Prefer not to say'),
        ('-', 'Any of the above'),
    )
    #Q35
    HOUSING = (
        ('1', 'Owner occupier - Lambeth leaseholder'),
        ('2', 'Owner occupier - private'),
        ('3', 'Rented from Housing Association'),
        ('4', 'Renting from Lambeth Council'),
        ('5', 'Rent from private landlord'),
        ('6', 'Shared ownership'),
        ('7', 'A residential home'),
        ('95', 'Other'),
        ('98', 'Refused'),
        ('-', 'Any of the above'),
    )
    name = models.CharField(max_length=200, unique=True)
    factor1 = models.CharField(max_length=2, choices=DISABILITY)
    factor2 = models.CharField(max_length=2, choices=BENEFITS)
    factor3 = models.CharField(max_length=2, choices=ACTIVITY)
    factor4 = models.CharField(max_length=2, choices=LLW)
    factor5 = models.CharField(max_length=2, choices=HOUSING)
    num_of_clusters = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '%s noc: %d' % (self.name, self.num_of_clusters)

    @staticmethod
    def get_factor_lists():
        return [Cluster.DISABILITY, Cluster.BENEFITS, Cluster.ACTIVITY, Cluster.LLW, Cluster.HOUSING]

class Subcluster(models.Model):
    #SERIAL field in spss 2016
    serial = models.CharField(max_length=8)
    #aka Cluster id
    group = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    subcluster = models.IntegerField()

    def __str__(self):
        return '%s %d' % (self.serial, self.group.id)
