from captcha.fields import CaptchaField
from django import forms
from django.utils.translation import gettext_lazy as _


class UserForm(forms.Form):
    username = forms.CharField(label=_('UserName'), max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_('Password'), max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # captcha = CaptchaField(label=_('Verification'))


class RegisterForm(forms.Form):
    # gender = (
    #     ('male', "男"),
    #     ('female', "女"),
    # )
    username = forms.CharField(label=_('UserName'), max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label=_('Password'), max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_('Confirm Password'), max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label=_('Email Address'), widget=forms.EmailInput(attrs={'class ': 'form-control'}))
    # sex = forms.ChoiceField(label='性别', choices=gender)

    usage = forms.CharField(label=_('Usage'), max_length=1024, widget=forms.Textarea(attrs={'class': 'form-control'}))
    affiliation = forms.CharField(label=_('Affiliation'), max_length=256,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label=_('Verification'))
