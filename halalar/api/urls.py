from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^log-in/$', views.LogInAPI.as_view(), name='api-log_in'),
    url(r'^sign-up/$', views.SignUpAPI.as_view(), name='api-sign_up'),
]