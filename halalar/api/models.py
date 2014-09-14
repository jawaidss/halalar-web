from django_countries.fields import CountryField
import hashlib
import random

from django.contrib.auth.models import User
from django.db import models

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
    age = models.SmallIntegerField()
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

class Message(models.Model):
    sender = models.ForeignKey(Profile, related_name='sent')
    recipient = models.ForeignKey(Profile, related_name='received')
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        ordering = ['timestamp']

    def __unicode__(self):
        return self.body