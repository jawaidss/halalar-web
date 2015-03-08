from push_notifications.models import APNSDevice, GCMDevice

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile, Message

class APIForm(object):
    def error_message(self):
        message = []

        for field, errors in sorted(self.errors.items()):
            if field == '__all__':
                message.append(' '.join(errors))
            else:
                message.append('%s: %s' % (field, ' '.join(errors)))

        return '\n'.join(message)

class AuthenticationForm(APIForm, AuthenticationForm):
    pass

class UserForm(APIForm, forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def save(self):
        user = super(UserForm, self).save()
        user.set_password(self.cleaned_data['password'])
        user.save()

        return user

class ProfileForm(APIForm, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'age', 'gender', 'city', 'country',
                  'religion', 'family', 'selfx', 'community', 'career']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['self'] = self.fields['selfx']
        del self.fields['selfx']

        if kwargs.get('instance') is not None:
            del self.fields['gender']

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()

        if 'self' in cleaned_data:
            cleaned_data['selfx'] = cleaned_data.pop('self')

        return cleaned_data

class MessageForm(APIForm, forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']

class APNSDeviceForm(APIForm, forms.ModelForm):
    class Meta:
        model = APNSDevice
        fields = ['registration_id']

class GCMDeviceForm(APIForm, forms.ModelForm):
    class Meta:
        model = GCMDevice
        fields = ['registration_id']