from django_countries.fields import CountryField
import hashlib
import random

from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
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
                'gender': self.get_gender_display(),
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