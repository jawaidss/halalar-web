from django.test import TestCase

from ..forms import UserForm, ProfileForm

class UserFormTestCase(TestCase):
    def test(self):
        form = UserForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'username': ['This field is required.'],
                                       'password': ['This field is required.'],
                                       'email': ['This field is required.']})

    def test_save(self):
        form = UserForm({'username': 'samad',
                         'password': 'temp123',
                         'email': 'samad@halalar.com'})
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.username, 'samad')
        self.assertTrue(user.check_password('temp123'))
        self.assertEqual(user.email, 'samad@halalar.com')

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

    def test_save(self):
        form = ProfileForm({'age': 23,
                            'career': 'test',
                            'city': 'Louisville',
                            'community': 'test',
                            'country': 'US',
                            'family': 'test',
                            'gender': 'male',
                            'religion': 'test',
                            'self': 'test'})
        self.assertTrue(form.is_valid())

        profile = form.save(commit=False)
        self.assertEqual(profile.age, 23)
        self.assertEqual(profile.career, 'test')
        self.assertEqual(profile.city, 'Louisville')
        self.assertEqual(profile.community, 'test')
        self.assertEqual(profile.country, 'US')
        self.assertEqual(profile.family, 'test')
        self.assertEqual(profile.gender, 'male')
        self.assertEqual(profile.religion, 'test')
        self.assertEqual(profile.selfx, 'test')