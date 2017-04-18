from django.forms import ModelForm
from clusters.models import Cluster

class ClusterForm(ModelForm):
    class Meta:
        model = Cluster
        fields = ['name', 'factor1', 'factor2', 'factor3', 'factor4', 'factor5']
        labels = {
            "name": "Name",
            "factor1": "Disability",
            "factor2": "Benefits",
            "factor3": "Economic activity",
            "factor4": "London Living Wage",
            "factor5": "Housing tenure",
        }
