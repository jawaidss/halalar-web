from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from captcha.conf import settings as captcha_settings

from ..forms import ContactForm

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
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(reverse('marketing-contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/contact.html')
        self.assertIsInstance(response.context['form'], ContactForm)
        self.assertEqual(len(mail.outbox), 0)

        captcha_settings.CAPTCHA_TEST_MODE = True
        response = self.client.post(reverse('marketing-contact'),
                                    data={'name': 'Samad',
                                          'email_address': 'samad@halalar.com',
                                          'message': 'Salaam',
                                          'captcha_0': 'passed',
                                          'captcha_1': 'passed'})
        self.assertRedirects(response, reverse('marketing-thanks'))
        self.assertEqual(len(mail.outbox), 1)

class ThanksViewTestCase(TestCase):
    def test_thanks_view(self):
        response = self.client.get(reverse('marketing-thanks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/thanks.html')

class AdminTestCase(TestCase):
    def test_admin(self):
        response = self.client.get(reverse('admin:index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, settings.SITE_NAME, count=2)

class SitemapTestCase(TestCase):
    def test_sitemap(self):
        response = self.client.get(reverse('django.contrib.sitemaps.views.sitemap'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/xml')