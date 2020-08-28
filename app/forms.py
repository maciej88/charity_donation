from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import User, Category, Institution


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=64, widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(max_length=64,  widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["password"].label = False
        self.fields["email"].label = False


class UserAddForm(UserCreationForm):
    first_name = forms.CharField(max_length=64, label='Imię', widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(max_length=64, label='Nazwisko', widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(max_length=64, label='Email', widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    password1 = forms.CharField(max_length=64, label='Hasło',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(
        max_length=64, label='Powtórz Hasło',
        widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1')

    def clean(self):
        clean_data =super().clean()
        password1 = clean_data.get('password1')
        password2 = clean_data.get('password2')
        if not password1 == password2:
            raise forms.ValidationError('Hasła nie są takie same!')

    def __init__(self, *args, **kwargs):
        super(UserAddForm, self).__init__(*args, **kwargs)
        self.fields["password2"].label = False
        self.fields["password1"].label = False
        self.fields["first_name"].label = False
        self.fields["last_name"].label = False
        self.fields["email"].label = False


# class ResetPasswordForm(forms.Form):
#     password1 = forms.CharField(max_length=64, label='Hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
#     password2 = forms.CharField(
#         max_length=64, label='Powtórz Hasło',
#         help_text='Hasła muszą być takie same', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
#
#     def clean(self):
#         clean_data = super().clean()
#         password1 = clean_data.get('password1')
#         password2 = clean_data.get('password1')
#         if not password2 == password1:
#             raise forms.ValidationError('Hasła nie są takie same!')
#
#     def __init__(self, *args, **kwargs):
#         super(ResetPasswordForm, self).__init__(*args, **kwargs)
#         self.fields["password2"].label = False
#         self.fields["password1"].label = False

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=64, label='Imię', widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(max_length=64, label='Nazwisko',
                                widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(max_length=64, label='Email', widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].label = False
        self.fields["last_name"].label = False
        self.fields["email"].label = False
