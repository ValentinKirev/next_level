from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from next_level.accounts.models import Profile
from next_level.utils import FormControlClassMixin, FormSelectClassMixin

UserModel = get_user_model()


class UserCreateForm(UserCreationForm, FormControlClassMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = 'Confirm Password'
        self.set_form_control_class()

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm, FormControlClassMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username or Email'
        self.error_messages['invalid_login'] = 'Please enter a correct username or email and valid password. Note that both fields are case-sensitive.'
        self.set_form_control_class()

    class Meta:
        model = UserModel
        fields = '__all__'


class ProfileEditForm(forms.ModelForm, FormControlClassMixin, FormSelectClassMixin):
    select_fields = ('gender', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_form_control_class()
        self.set_form_select_class()

    class Meta:
        model = Profile
        exclude = ['user']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'profile_picture': 'Profile Picture'
        }
