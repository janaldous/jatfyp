from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'clusters'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<cluster_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^new', views.create_cluster, name='new'),
    url(r'^map', views.map, name='map'),
    url(r'^json/(?P<cluster_id>[0-9]+)', views.json, name='json'),
    url(r'^survey/(?P<question>[0-9A-Za-z]+)', views.see_question_answers, name='question'),
    url(r'^survey', views.survey_questions, name='survey'),
    url(r'^(?P<cluster_id>[0-9]+)/compare', views.compare, name='compare'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
