# encoding:utf-8
import re

from django import forms

from .models import UserAsk


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'phone_num', 'course_ask']

    def clean_phone_num(self):
        reg = r'^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$'
        phone_mun = self.cleaned_data['phone_num']
        if re.match(reg, phone_mun):
            return phone_mun
        else:
            raise forms.ValidationError(u'电话号码错误', code='phone_error')
