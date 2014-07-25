from django.conf.urls import patterns, include, url

from django.contrib import admin
from send import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^send/', include('send.urls', namespace = "send")),

    # Examples:
    # url(r'^$', 'Mandrill.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
                    
)
