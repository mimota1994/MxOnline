#_*_coding:utf-8_*_
__author__ = 'bobby'
__date__ = '2018-03-13 22:11'
from django import forms
from captcha.fields import CaptchaField


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


