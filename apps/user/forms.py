from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput
from .models import User
from django.contrib.auth import authenticate
from modules.helpers import update_avatar
from .models import UserProfile
from alpha.settings import DEBUG

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class AuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Никнейм',
                                                       'label' : 'username', 'name' : 'username'}))

    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль',
                                                       'label' : 'password', 'name' : 'password'}))

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
                                                             'name':'remember', 'id': 'customCheckLogin',
                                                              'class': 'custom-control-input'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        remember_me = self.cleaned_data.get('remember_me')

        # if not remember_me:
        #     self.request.session.set_expiry(0)

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RegisterForm(UserCreationForm):

    #TODO add errors callback

    error_messages = {
        'password_mismatch': _("Введенные пароли не совпадают"),
    }

    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Никнейм',
                                                       'label': 'username', 'name': 'username'}))

    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль',
                                                           'label': 'password1', 'name': 'password1'}))

    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль',
                                                           'label': 'password2', 'name': 'password2'}))

    email = forms.CharField(widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Почта',
                                                           'label': 'email', 'name': 'email'}))

    class Meta:
        model = User
        fields = ("username", 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user.refresh_from_db()
            # TODO: Connect userprofile
            if DEBUG == True:
                user.profile.confirmed = True
            update_avatar(self.data['avatar'], user)
            user.save()

        # print(profile)
        return user


class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(max_length=User._meta.get_field('username').max_length,
                                                     widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Новый никнейм',
                                                       'label': 'username', 'name': 'username'}))

    email = forms.CharField(max_length=User._meta.get_field('email').max_length,
                            widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Новая почта',
                                                     'label': 'email', 'name': 'email'}))

    first_name = forms.CharField(max_length=UserProfile._meta.get_field('first_name').max_length,
                                 widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя',
                                                       'label': 'first_name', 'name': 'first_name'}))

    last_name = forms.CharField(max_length=UserProfile._meta.get_field('last_name').max_length,
                                widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия',
                                                       'label': 'last_name', 'name': 'last_name'}))

    github = forms.URLField(required=False, max_length=UserProfile._meta.get_field('github').max_length,
                                 widget=forms.URLInput(attrs={'placeholder': "Ссылка на ваш профиль",
                                                              'id': 'input-github',
                                                              'name': 'github',
                                                              'class': 'form-control form-control-alternative',
                                                              }))

    telegram = forms.URLField(required=False, max_length=UserProfile._meta.get_field('telegram').max_length,
                                 widget=forms.URLInput(attrs={'placeholder': "Ссылка на ваш профиль",
                                                              'id': 'telegram',
                                                              'name': 'telegram',
                                                              'class': 'form-control form-control-alternative',
                                                              }))

    linked_in = forms.URLField(required=False, max_length=UserProfile._meta.get_field('linked_in').max_length,
                                 widget=forms.URLInput(attrs={'placeholder': "Ссылка на ваш профиль",
                                                              'id': 'linked_in',
                                                              'name': 'linked_in',
                                                              'class': 'form-control form-control-alternative',
                                                              }))

    vk = forms.URLField(required=False, max_length=UserProfile._meta.get_field('vk').max_length,
                                 widget=forms.URLInput(attrs={'placeholder': "Ссылка на ваш профиль",
                                                              'id': 'vk',
                                                              'name': 'vk',
                                                              'class': 'form-control form-control-alternative',
                                                              }))

    bio = forms.CharField(required=False, max_length=UserProfile._meta.get_field('bio').max_length,
                          widget=forms.Textarea(attrs={'placeholder': "Любые детали такие как возраст, страна или город.",
                                                       "rows": "4",
                                                       'id': 'bio',
                                                       "maxlength": UserProfile._meta.get_field('bio').max_length,
                                                       'name': 'bio',
                                                       'class': 'form-control form-control-alternative'}))

    class Meta:
        model = UserProfile
        fields = ("username", 'email', 'first_name', 'last_name', 'github', 'telegram',
                  'linked_in', 'vk', 'bio')