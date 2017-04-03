#from django import forms
from django.forms import ModelForm
from clusters.models import Cluster

class ClusterForm(ModelForm):
    class Meta:
        model = Cluster
        fields = ['name', 'factor1', 'factor2', 'factor3', 'factor4', 'factor5']
