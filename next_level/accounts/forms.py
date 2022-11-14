from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = 'Confirm Password'
        self.set_class()

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']

    def set_class(self):
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
