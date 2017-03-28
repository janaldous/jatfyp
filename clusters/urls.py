from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'clusters'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<cluster_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<cluster_id>[0-9]+)/stats/$', views.stats, name='stats'),
    url(r'^(?P<cluster_id>[0-9]+)/subclusters_list', views.subclusters_list, name='subclusters_list'),
    url(r'^(?P<cluster_id>[0-9]+)/subcluster/(?P<subcluster_id>[0-9]+)', views.subcluster_detail, name='subcluster_detail'),
    url(r'^new', views.create_cluster, name='new'),
    url(r'^(?P<cluster_id>[0-9]+)/increase/', views.increase_num_of_clusters, name='increase'),
    url(r'^(?P<cluster_id>[0-9]+)/decrease/', views.decrease_num_of_clusters, name='decrease'),
    url(r'^map', views.map, name='map'),
    url(r'^test', views.test, name='test'),
    url(r'^groupcompare/', views.group_compare, name='groupcompare'),
    url(r'^json/(?P<cluster_id>[0-9]+)', views.json, name='json'),#map
    url(r'^jsonv2/(?P<cluster_id>[0-9]+)', views.jsonv2, name='jsonv2'),#ward chart
    url(r'^json3/(?P<cluster_id>[0-9]+)/(?P<question_id>[A-Z0-9_]+)', views.json3, name='json3'),
    url(r'^json4/(?P<cluster_id>[0-9]+)/(?P<question_id>[A-Z0-9_]+)/(?P<choice_id>[0-9]+)', views.json4, name='json4'),#ward chart redraw function
    url(r'^jsoncompare/(?P<question_id>[A-Z0-9_]+)/(?P<choice_id>[0-9]+)', views.jsoncompare, name='jsoncompare'),#for group compare view
    url(r'^json2/(?P<cluster_id>[0-9]+)/(?P<question_id>[A-Z0-9_]+)/(?P<choice_id>[0-9]+)', views.json2, name='json2'),#for map change
    url(r'^survey/(?P<question>[0-9A-Za-z_]+)', views.see_question_answers, name='question'),
    url(r'^survey', views.survey_questions, name='survey'),
    url(r'^(?P<cluster_id>[0-9]+)/compare', views.compare, name='compare'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
