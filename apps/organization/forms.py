#_*_coding:utf-8_*_
__author__ = 'bobby'
__date__ = '2018-03-24 20:33'
from django import  forms

from operation.models import UserAsk


class AnotherUserForm(forms.ModelForm):
    class Meta:
        model=UserAsk
        fields=['name','mobile','course_name']
