from django.core.urlresolvers import reverse
from django.test import TestCase

class PrivacyPolicyViewTestCase(TestCase):
    def test_privacy_policy_view(self):
        response = self.client.get(reverse('legal-privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'legal/privacy_policy.html')

class TermsOfServiceViewTestCase(TestCase):
    def test_terms_of_service_view(self):
        response = self.client.get(reverse('legal-terms_of_service'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'legal/terms_of_service.html')