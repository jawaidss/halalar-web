from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from marketing import views as marketing_views

urlpatterns = patterns('',
    url(r'^$', marketing_views.HomeView.as_view(), name='marketing-home'),
    url(r'^marketing/', include('marketing.urls')),
    url(r'^legal/', include('legal.urls')),
    url(r'^admin/', include(admin.site.urls)),
)