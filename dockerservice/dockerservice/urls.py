from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dockerservice.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^logout/', 'dockerservice.views.logout'),		
    url(r'^$', 'dockerservice.views.index'),		
    url(r'^', include('userside.urls')),
)
