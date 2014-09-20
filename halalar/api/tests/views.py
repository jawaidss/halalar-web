import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from . import TEST_DATA, create_user, create_profile
from ..models import Profile

class LogInAPITestCase(TestCase):
    def test_log_in_api_invalid(self):
        response = self.client.post(reverse('api-log_in'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'message': 'password: This field is required.\nusername: This field is required.',
                                                        'status': 'error'})

    def test_log_in_api_valid(self):
        user = create_user()

        response = self.client.post(reverse('api-log_in'), {'username': TEST_DATA[0]['username'],
                                                            'password': TEST_DATA[0]['password']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'message': '',
                                                        'status': 'error'})

        profile = create_profile(user)

        response = self.client.post(reverse('api-log_in'), {'username': TEST_DATA[0]['username'],
                                                            'password': TEST_DATA[0]['password']})
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
        response = self.client.post(reverse('api-sign_up'), TEST_DATA[0])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'data': {'token': Profile.objects.get().token},
                                                        'status': 'success'})

class GetProfileAPITestCase(TestCase):
    def setUp(self):
        user = create_user()
        self.profile = create_profile(user)

    def test_get_profile_api_invalid(self):
        response = self.client.get(reverse('api-get_profile'))
        self.assertEqual(response.status_code, 404)

    def test_get_profile_api_valid(self):
        response = self.client.get(reverse('api-get_profile'), {'token': self.profile.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'data': {'profile': self.profile.serialize()},
                                                        'status': 'success'})

    def test_get_random_profile_api_invalid(self):
        response = self.client.get(reverse('api-get_random_profile'))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('api-get_random_profile'), {'token': self.profile.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'message': '',
                                                        'status': 'error'})

    def test_get_random_profile_api_valid(self):
        user = create_user(1)
        profile = create_profile(user, 1)

        response = self.client.get(reverse('api-get_random_profile'), {'token': self.profile.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'data': {'profile': profile.serialize(False)},
                                                        'status': 'success'})

    def test_get_specific_profile_api_invalid(self):
        response = self.client.get(reverse('api-get_specific_profile', kwargs={'username': self.profile.user.username}))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('api-get_specific_profile', kwargs={'username': self.profile.user.username}), {'token': self.profile.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'message': '',
                                                        'status': 'error'})

        user = create_user(1)
        profile = create_profile(user, 1)

        response = self.client.get(reverse('api-get_specific_profile', kwargs={'username': self.profile.user.username}), {'token': self.profile.token})
        self.assertEqual(response.status_code, 404)

    def test_get_specific_profile_api_valid(self):
        user = create_user(1)
        profile = create_profile(user, 1)

        response = self.client.get(reverse('api-get_specific_profile', kwargs={'username': user.username}), {'token': self.profile.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'data': {'profile': profile.serialize(False)},
                                                        'status': 'success'})