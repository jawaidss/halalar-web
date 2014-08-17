from django.core.urlresolvers import reverse
from django.test import TestCase

class HomeViewTestCase(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('marketing-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/home.html')

class AboutViewTestCase(TestCase):
    def test_about_view(self):
        response = self.client.get(reverse('marketing-about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/about.html')

class ContactViewTestCase(TestCase):
    def test_contact_view(self):
        response = self.client.get(reverse('marketing-contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/contact.html')

class ThanksViewTestCase(TestCase):
    def test_thanks_view(self):
        response = self.client.get(reverse('marketing-thanks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/thanks.html')