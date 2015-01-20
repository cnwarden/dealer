from django.conf.urls import patterns, include, url, handler400
from django.conf import settings
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dealerweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/',  include(admin.site.urls)),
    url(r'^dealer/', include('dealer.urls')),
    url(r'^none/',   handler400)
)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
