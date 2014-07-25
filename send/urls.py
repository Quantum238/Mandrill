from django.conf.urls import patterns, url

from send import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name = 'index'),
                       url(r'^(?P<message_id>\d+)/$',views.detail, name = 'detail'),
                       url(r'^(?P<message_id>\d+)/confimation$',views.confirmation,name = 'confirmation'),
                       url(r'^(?P<message_id>\d+)/see_stats$',views.see_stats,name = 'see_stats'),
                       url(r'^get_stats$',views.get_stats,name='get_stats'),
                       )
