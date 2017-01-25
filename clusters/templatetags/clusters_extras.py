from django import template
from ..models import Cluster
register = template.Library()

@register.inclusion_tag('clusters/clusters.html')
def cluster_list():
    """returns list of all clusters"""
    clusters = Cluster.objects.all()
    return {'clusters':clusters}
