from django.views.generic.base import TemplateView

class PrivacyPolicyView(TemplateView):
    template_name = 'legal/privacy_policy.html'

class TermsOfServiceView(TemplateView):
    template_name = 'legal/terms_of_service.html'