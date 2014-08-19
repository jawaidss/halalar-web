from django.conf import settings
from django.core import mail
from django.test import TestCase

from captcha.conf import settings as captcha_settings

from ..forms import ContactForm

class ContactFormTestCase(TestCase):
    def test_send_mail(self):
        form = ContactForm({'name': 'Samad',
                            'email_address': 'samad@halalar.com',
                            'message': 'Salaam',
                            'captcha_0': 'passed',
                            'captcha_1': 'passed'})

        captcha_settings.CAPTCHA_TEST_MODE = True
        self.assertTrue(form.is_valid())

        form.send_mail('127.0.0.1')
        self.assertEqual(len(mail.outbox), 1)

        message = mail.outbox[0]

        self.assertEqual(message.subject, 'Message from Samad')
        self.assertEqual(message.body, '''Name: Samad
Email address: samad@halalar.com
Phone number: 
Message: Salaam
IP address: 127.0.0.1''')
        self.assertEqual(message.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(message.to, [settings.DEFAULT_FROM_EMAIL])
        self.assertEqual(message.cc, [])
        self.assertEqual(message.bcc, [])
        self.assertEqual(message.attachments, [])