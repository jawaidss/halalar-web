from django_countries.fields import CountryField

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    user = models.OneToOneField(User)
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

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent')
    recipient = models.ForeignKey(User, related_name='received')
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        ordering = ['timestamp']

    def __unicode__(self):
        return self.body