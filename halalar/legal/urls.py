from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^privacy-policy/$', views.PrivacyPolicyView.as_view(), name='legal-privacy_policy'),
    url(r'^terms-of-service/$', views.TermsOfServiceView.as_view(), name='legal-terms_of_service'),
]