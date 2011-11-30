from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chattr.views.home', name='home'),
    # url(r'^chattr/', include('chattr.foo.urls')),
	
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	
	# Chat URL set
	url(r'^', include('chattr.jqchat.urls')),
    
    (r'^interests/$', 'interests.views.interest_manage_view'),
)

