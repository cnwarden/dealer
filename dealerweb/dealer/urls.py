from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$',      'dealer.views.index'),
    url(r'^home/',      'dealer.views.home'),
    url(r'^stock/(\d+)$', 'dealer.views.stock')
)
