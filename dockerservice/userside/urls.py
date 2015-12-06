from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^home/$', 'userside.views.home'),
    url(r'^dashboard/$', 'userside.views.manage'),
    url(r'^destroy/(?P<name>\w+)/$', 'userside.views.destroy'),
    url(r'^check/(?P<user>\w+)/$', 'userside.views.checkStatus'),
)
