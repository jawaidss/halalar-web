from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Profile

class ProfileTestCase(TestCase):
    def test_save(self):
        # tests that a token is generated on save
        # if it is not given
        user = User.objects.create_user('user1')
        profile = Profile(user=user, age=0)
        profile.save()
        self.assertEqual(len(profile.token), 40)

        # if it is null
        user = User.objects.create_user('user2')
        profile = Profile(user=user, age=0, token=None)
        profile.save()
        self.assertEqual(len(profile.token), 40)

        # if it is blank
        user = User.objects.create_user('user3')
        profile = Profile(user=user, age=0, token='')
        profile.save()
        self.assertEqual(len(profile.token), 40)
        old_token = profile.token

        # tests that the token does not change on save
        profile.save()
        new_token = profile.token
        self.assertEqual(old_token, new_token)

        # tests that a given token is not overridden on save
        user = User.objects.create_user('user4')
        profile = Profile(user=user, age=0, token='token')
        profile.save()
        self.assertEqual(profile.token, 'token')