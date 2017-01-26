from django.conf.urls import url

from . import views

app_name = 'clusters'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<cluster_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^new', views.create_cluster, name='new'),
]
