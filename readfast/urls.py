from django.conf.urls import patterns, url

from readfast import views

urlpatterns = patterns('',
    url(r'^$', views.TestIndexView.as_view(), name='index'),
    url(r'^(?P<test_id>\d+)/$', views.TestDetailView.as_view(), name='detail'),
)