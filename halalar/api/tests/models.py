from django.contrib.auth.models import User
from django.test import TestCase

from . import TEST_DATA, BODY, create_user, create_profile, create_message
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

    def test_serialize(self):
        user = create_user()
        profile = create_profile(user)
        expected = {'age': TEST_DATA[0]['age'],
                    'career': TEST_DATA[0]['career'],
                    'city': TEST_DATA[0]['city'],
                    'community': TEST_DATA[0]['community'],
                    'country': TEST_DATA[0]['country'],
                    'email': TEST_DATA[0]['email'],
                    'family': TEST_DATA[0]['family'],
                    'gender': TEST_DATA[0]['gender'].capitalize(),
                    'religion': TEST_DATA[0]['religion'],
                    'self': TEST_DATA[0]['self'],
                    'username': TEST_DATA[0]['username']}

        self.assertEqual(profile.serialize(), expected)

        del expected['email']

        self.assertEqual(profile.serialize(False), expected)

class MessageTestCase(TestCase):
    def test_serialize(self):
        sender = create_profile(create_user())
        recipient = create_profile(create_user(1), 1)
        message = create_message(sender, recipient)

        expected = {'sender': TEST_DATA[0]['username'],
                    'recipient': TEST_DATA[1]['username'],
                    'timestamp': 'now',
                    'body': BODY}

        self.assertEqual(message.serialize(), expected)