from django import forms
from django.conf import settings
from django.core.mail import EmailMessage

from captcha.fields import CaptchaField
from localflavor.us.forms import USPhoneNumberField

class ContactForm(forms.Form):
    name = forms.CharField()
    email_address = forms.EmailField()
    phone_number = USPhoneNumberField(required=False)
    message = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()

    def send_mail(self):
        email_message = EmailMessage()
        email_message.subject = 'Message from %s' % self.cleaned_data['name']
        email_message.body = '''
Name: %(name)s
Email address: %(email_address)s
Phone number: %(phone_number)s
Message: %(message)s
        '''.strip() % self.cleaned_data
        email_message.to = [settings.DEFAULT_FROM_EMAIL]
        email_message.send()