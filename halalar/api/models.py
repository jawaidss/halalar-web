from datetime import datetime, timedelta
from django_countries.fields import CountryField
import hashlib
import mailchimp
import random

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage, send_mail
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
from django.db import models

MINIMUM_AGE = 18

def _random_token(username):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    return hashlib.sha1(salt + username).hexdigest()

class Profile(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    user = models.OneToOneField(User)
    token = models.CharField(max_length=40, unique=True, editable=False)
    age = models.SmallIntegerField(validators=[MinValueValidator(MINIMUM_AGE)])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    city = models.CharField(max_length=100)
    country = CountryField(default='US')
    religion = models.TextField()
    family = models.TextField()
    selfx = models.TextField('self')
    community = models.TextField()
    career = models.TextField()

    class Meta:
        ordering = ['user']

    def __unicode__(self):
        return self.user.username

    def save(self, **kwargs):
        if self.id is None and not self.token and self.user_id is not None:
            self.token = _random_token(self.user.username)

        super(Profile, self).save(**kwargs)

    def serialize(self, include_email=True):
        data = {'username': self.user.username,
                'age': self.age,
                'gender': self.gender,
                'city': self.city,
                'country': self.country.code,
                'religion': self.religion,
                'family': self.family,
                'self': self.selfx,
                'community': self.community,
                'career': self.career}

        if include_email:
            data['email'] = self.user.email

        return data

    def send_delayed_welcome_email(self):
        site = Site.objects.get_current()

        subject = site.name
        message = '''Salaam,

I'm Sikander, the creator of %s. Thanks for signing up! I wanted to reach out to see if you needed any help getting started.

Best,

--
Sikander Chowhan
www.%s''' % (site.name, site.domain)

        from_email = 'Sikander Chowhan <sikander@%s>' % site.domain
        to = [self.user.email]

        email = EmailMessage(subject, message, from_email, to)
        email.send_at = datetime.now() + timedelta(days=1)
        email.send()

    def send_signup_notification_email(self):
        site = Site.objects.get_current()

        subject = self.user.username
        message = '''Username: %(username)s
Email: %(email)s

Age: %(age)s
Gender: %(gender)s
City: %(city)s
Country: %(country)s

Religion: %(religion)s

Family: %(family)s

Self: %(self)s

Community: %(community)s

Career: %(career)s

https://%(domain)s%(user_url)s
https://%(domain)s%(profile_url)s''' % {'username': self.user.username,
                                'email': self.user.email,
                                'age': self.age,
                                'gender': self.get_gender_display(),
                                'city': self.city,
                                'country': self.country.name,
                                'religion': self.religion,
                                'family': self.family,
                                'self': self.selfx,
                                'community': self.community,
                                'career': self.career,
                                'domain': site.domain,
                                'user_url': reverse('admin:auth_user_change', args=[self.user.pk]),
                                'profile_url': reverse('admin:api_profile_change', args=[self.pk])}

        from_email = 'sikander@%s' % site.domain
        recipient_list = [settings.ASANA_EMAIL]

        send_mail(subject, message, from_email, recipient_list)

    def subscribe_to_mailchimp_list(self):
        m = mailchimp.Mailchimp()
        m.lists.subscribe(settings.MAILCHIMP_LIST_ID,
                          {'email': self.user.email},
                          double_optin=False,
                          update_existing=True)

class Message(models.Model):
    sender = models.ForeignKey(Profile, related_name='sent')
    recipient = models.ForeignKey(Profile, related_name='received')
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        ordering = ['timestamp']
        get_latest_by = 'timestamp'

    def __unicode__(self):
        return self.body

    def serialize(self):
        return {'sender': self.sender.user.username,
                'recipient': self.recipient.user.username,
                'timestamp': naturaltime(self.timestamp),
                'body': self.body}