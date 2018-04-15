#_*_coding:utf-8_*_
__author__ = 'bobby'
__date__ = '2018-03-13 22:11'
from django import forms
from captcha.fields import CaptchaField
import re

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ForgetpwdForm(forms.Form):
    email=forms.EmailField(required=True)
    captcha=CaptchaField(error_messages={"invalid":"验证码错误"})


class ModeifyPwdForm(forms.Form):
    password1=forms.CharField(required=True)
    password2=forms.CharField(required=True)


class UserModeifyForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['nick_name','gender','address','mobile','email']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalide")


class UserImageForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['image']


class EmailModeifyForm(forms.Form):
    eamil=forms.EmailField(required=True)