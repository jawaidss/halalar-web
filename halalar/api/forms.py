from django import forms
from django.contrib.auth.models import User

from .models import Profile

class UserForm(forms.ModelForm):
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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'gender', 'city', 'country',
                  'religion', 'family', 'selfx', 'community', 'career']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['self'] = self.fields['selfx']
        del self.fields['selfx']

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()

        if 'self' in cleaned_data:
            cleaned_data['selfx'] = cleaned_data.pop('self')

        return cleaned_data