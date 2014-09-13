from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from .sitemap import sitemaps

from marketing import views as marketing_views

admin.site.site_title = '%s admin' % settings.SITE_NAME
admin.site.site_header = '%s administration' % settings.SITE_NAME

urlpatterns = patterns('',
    url(r'^$', marketing_views.HomeView.as_view(), name='marketing-home'),
    url(r'^marketing/', include('marketing.urls')),
    url(r'^legal/', include('legal.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
