from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shell.views.home', name='home'),
    # url(r'^shell/', include('shell.foo.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sentry/', include('sentry.web.urls')),
    #url(r'^status/?', include('overseer.urls', namespace='overseer')),
    url(r'^api/v1/', include('shell.apps.api.urls')),
    url(r'^', include('shell.apps.frontend.urls')),
)
