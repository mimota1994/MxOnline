#_*_coding:utf-8_*_
__author__ = 'bobby'
__date__ = '2018-03-24 20:33'
import re
from django import  forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model=UserAsk
        fields=['name','mobile','course_name']

    def clean_mobile(self):
        mobile=self.cleaned_data['mobile']
        REGEX_MOBILE="^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p =re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法",code="mobile_invalide")