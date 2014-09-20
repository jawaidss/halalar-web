import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from . import TEST_DATA
from ..models import Profile

class LogInAPITestCase(TestCase):
    def test_log_in_api_invalid(self):
        response = self.client.post(reverse('api-log_in'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'message': 'password: This field is required.\nusername: This field is required.',
                                                        'status': 'error'})

    def test_log_in_api_valid(self):
        user = User.objects.create_user(TEST_DATA['username'],
                                        email=TEST_DATA['email'],
                                        password=TEST_DATA['password'])

        response = self.client.post(reverse('api-log_in'), data={'username': TEST_DATA['username'],
                                                                 'password': TEST_DATA['password']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'message': '',
                                                        'status': 'error'})

        profile = Profile.objects.create(user=user,
                                         age=TEST_DATA['age'],
                                         gender=TEST_DATA['gender'],
                                         city=TEST_DATA['city'],
                                         country=TEST_DATA['country'],
                                         religion=TEST_DATA['religion'],
                                         family=TEST_DATA['family'],
                                         selfx=TEST_DATA['self'],
                                         community=TEST_DATA['community'],
                                         career=TEST_DATA['career'])

        response = self.client.post(reverse('api-log_in'), data={'username': TEST_DATA['username'],
                                                                 'password': TEST_DATA['password']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'data': {'token': profile.token},
                                                        'status': 'success'})

class SignUpAPITestCase(TestCase):
    def test_sign_up_api_invalid(self):
        response = self.client.post(reverse('api-sign_up'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'message': 'email: This field is required.\npassword: This field is required.\nusername: This field is required.\nage: This field is required.\ncareer: This field is required.\ncity: This field is required.\ncommunity: This field is required.\ncountry: This field is required.\nfamily: This field is required.\ngender: This field is required.\nreligion: This field is required.\nself: This field is required.',
                                                        'status': 'error'})

    def test_sign_up_api_valid(self):
        response = self.client.post(reverse('api-sign_up'), data=TEST_DATA)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'data': {'token': Profile.objects.get().token},
                                                        'status': 'success'})