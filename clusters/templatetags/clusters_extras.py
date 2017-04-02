from django import template
from ..models import Cluster
register = template.Library()

@register.inclusion_tag('clusters/clusters.html')
def cluster_list():
    """returns list of all clusters"""
    clusters = Cluster.objects.all()
    return {'clusters':clusters}

@register.simple_tag(name='percent')
def percent(x, y):
    p = (float(x)/float(y))*100
    return "%.1f" % p

@register.simple_tag(name='choice_as_str')
def choice_as_str(factor, x):
    """ let x = Cluster choice """
    factor = int(factor)-1
    d = dict(Cluster.get_factor_lists()[factor])
    return d[x]
