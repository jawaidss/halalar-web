import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from . import TEST_DATA, BODY, create_user, create_profile, create_message
from ..models import Profile, Message

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

class AuthenticatedAPITestCase(TestCase):
    def setUp(self):
        user = create_user()
        self.profile = create_profile(user)

class GetProfileAPITestCase(AuthenticatedAPITestCase):
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

        create_profile(create_user(1), 1)

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

class EditProfileAPITestCase(AuthenticatedAPITestCase):
    def test_edit_profile_api_invalid(self):
        response = self.client.post(reverse('api-edit_profile'))
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse('api-edit_profile'), {'token': self.profile.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'message': 'age: This field is required.\ncareer: This field is required.\ncity: This field is required.\ncommunity: This field is required.\ncountry: This field is required.\nfamily: This field is required.\nreligion: This field is required.\nself: This field is required.',
                                                        'status': 'error'})

    def test_edit_profile_api_valid(self):
        data = {'token': self.profile.token}
        data.update(TEST_DATA[1])
        response = self.client.post(reverse('api-edit_profile'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        profile = Profile.objects.get()
        self.assertEqual(json.loads(response.content), {'data': {'profile': profile.serialize()},
                                                        'status': 'success'})
        self.assertEqual(profile.age, TEST_DATA[1]['age'])
        self.assertEqual(profile.career, TEST_DATA[1]['career'])
        self.assertEqual(profile.city, TEST_DATA[1]['city'])
        self.assertEqual(profile.community, TEST_DATA[1]['community'])
        self.assertEqual(profile.country, TEST_DATA[1]['country'])
        self.assertEqual(profile.family, TEST_DATA[1]['family'])
        self.assertEqual(profile.religion, TEST_DATA[1]['religion'])
        self.assertEqual(profile.selfx, TEST_DATA[1]['self'])
        self.assertNotEqual(profile.gender, TEST_DATA[1]['gender'])

class GetConversationsAPITestCase(AuthenticatedAPITestCase):
    def test_get_conversations_api_invalid(self):
        response = self.client.get(reverse('api-get_conversations'))
        self.assertEqual(response.status_code, 404)

    def test_get_conversations_api_valid(self):
        response = self.client.get(reverse('api-get_conversations'), {'token': self.profile.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'data': {'messages': []},
                                                        'status': 'success'})

        recipient = create_profile(create_user(1), 1)
        message = create_message(self.profile, recipient)

        response = self.client.get(reverse('api-get_conversations'), {'token': self.profile.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'data': {'messages': [message.serialize()]},
                                                        'status': 'success'})

        message = create_message(recipient, self.profile)

        response = self.client.get(reverse('api-get_conversations'), {'token': self.profile.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'data': {'messages': [message.serialize()]},
                                                        'status': 'success'})

class GetConversationAPITestCase(AuthenticatedAPITestCase):
    def test_get_conversation_api_invalid(self):
        response = self.client.get(reverse('api-get_conversation', kwargs={'username': self.profile.user.username}))
        self.assertEqual(response.status_code, 404)

    def test_get_conversation_api_valid(self):
        recipient = create_profile(create_user(1), 1)

        response = self.client.get(reverse('api-get_conversation', kwargs={'username': recipient.user.username}), {'token': self.profile.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'data': {'messages': []},
                                                        'status': 'success'})

        messages = [create_message(self.profile, recipient).serialize()]

        response = self.client.get(reverse('api-get_conversation', kwargs={'username': recipient.user.username}), {'token': self.profile.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'data': {'messages': messages},
                                                        'status': 'success'})

        messages.append(create_message(recipient, self.profile).serialize())

        response = self.client.get(reverse('api-get_conversation', kwargs={'username': recipient.user.username}), {'token': self.profile.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'data': {'messages': messages},
                                                        'status': 'success'})

class SendMessageAPITestCase(AuthenticatedAPITestCase):
    def test_send_message_api_invalid(self):
        recipient = create_profile(create_user(1), 1)

        response = self.client.post(reverse('api-send_message', kwargs={'username': recipient.user.username}))
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse('api-send_message', kwargs={'username': self.profile.user.username}), {'token': self.profile.token})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse('api-send_message', kwargs={'username': recipient.user.username}), {'token': self.profile.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content), {'message': 'body: This field is required.',
                                                        'status': 'error'})

    def test_send_message_api_valid(self):
        recipient = create_profile(create_user(1), 1)

        response = self.client.post(reverse('api-send_message', kwargs={'username': recipient.user.username}), {'token': self.profile.token, 'body': BODY})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        message = Message.objects.get()
        self.assertEqual(json.loads(response.content), {'data': {'message': message.serialize()},
                                                        'status': 'success'})
        self.assertEqual(message.sender.user.username, TEST_DATA[0]['username'])
        self.assertEqual(message.recipient.user.username, TEST_DATA[1]['username'])
        self.assertEqual(message.body, BODY)