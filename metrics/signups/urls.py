from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'signups.views.index'),
    url(r'^add/$', 'signups.views.create'),

)