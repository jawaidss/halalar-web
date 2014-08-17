from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^about/$', views.AboutView.as_view(), name='marketing-about'),
    url(r'^contact/$', views.ContactView.as_view(), name='marketing-contact'),
    url(r'^contact/thanks/$', views.ThanksView.as_view(), name='marketing-thanks'),
]