from django.test import TestCase

from . import TEST_DATA
from ..forms import AuthenticationForm, UserForm, ProfileForm

class AuthenticationFormTestCase(TestCase):
    def test(self):
        form = AuthenticationForm(data={'username': TEST_DATA[0]['username'],
                                        'password': TEST_DATA[0]['password']})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'__all__': ['Please enter a correct username and password. Note that both fields may be case-sensitive.']})
        self.assertEqual(form.error_message(), 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

class UserFormTestCase(TestCase):
    def test(self):
        form = UserForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'username': ['This field is required.'],
                                       'password': ['This field is required.'],
                                       'email': ['This field is required.']})
        self.assertEqual(form.error_message(), 'email: This field is required.\npassword: This field is required.\nusername: This field is required.')

    def test_save(self):
        form = UserForm({'username': TEST_DATA[0]['username'],
                         'password': TEST_DATA[0]['password'],
                         'email': TEST_DATA[0]['email']})
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.username, TEST_DATA[0]['username'])
        self.assertTrue(user.check_password(TEST_DATA[0]['password']))
        self.assertEqual(user.email, TEST_DATA[0]['email'])

class ProfileFormTestCase(TestCase):
    def test(self):
        form = ProfileForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'age': ['This field is required.'],
                                       'career': ['This field is required.'],
                                       'city': ['This field is required.'],
                                       'community': ['This field is required.'],
                                       'country': ['This field is required.'],
                                       'family': ['This field is required.'],
                                       'gender': ['This field is required.'],
                                       'religion': ['This field is required.'],
                                       'self': ['This field is required.']})

        form = ProfileForm({'age': 0,
                            'gender': 'foo',
                            'country': 'XX'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'age': ['Ensure this value is greater than or equal to 18.'],
                                       'career': ['This field is required.'],
                                       'city': ['This field is required.'],
                                       'community': ['This field is required.'],
                                       'country': ['Select a valid choice. XX is not one of the available choices.'],
                                       'family': ['This field is required.'],
                                       'gender': ['Select a valid choice. foo is not one of the available choices.'],
                                       'religion': ['This field is required.'],
                                       'self': ['This field is required.']})
        self.assertEqual(form.error_message(), 'age: Ensure this value is greater than or equal to 18.\ncareer: This field is required.\ncity: This field is required.\ncommunity: This field is required.\ncountry: Select a valid choice. XX is not one of the available choices.\nfamily: This field is required.\ngender: Select a valid choice. foo is not one of the available choices.\nreligion: This field is required.\nself: This field is required.')

    def test_save(self):
        form = ProfileForm({'age': TEST_DATA[0]['age'],
                            'career': TEST_DATA[0]['career'],
                            'city': TEST_DATA[0]['city'],
                            'community': TEST_DATA[0]['community'],
                            'country': TEST_DATA[0]['country'],
                            'family': TEST_DATA[0]['family'],
                            'gender': TEST_DATA[0]['gender'],
                            'religion': TEST_DATA[0]['religion'],
                            'self': TEST_DATA[0]['self']})
        self.assertTrue(form.is_valid())

        profile = form.save(commit=False)
        self.assertEqual(profile.age, TEST_DATA[0]['age'])
        self.assertEqual(profile.career, TEST_DATA[0]['career'])
        self.assertEqual(profile.city, TEST_DATA[0]['city'])
        self.assertEqual(profile.community, TEST_DATA[0]['community'])
        self.assertEqual(profile.country, TEST_DATA[0]['country'])
        self.assertEqual(profile.family, TEST_DATA[0]['family'])
        self.assertEqual(profile.gender, TEST_DATA[0]['gender'])
        self.assertEqual(profile.religion, TEST_DATA[0]['religion'])
        self.assertEqual(profile.selfx, TEST_DATA[0]['self'])