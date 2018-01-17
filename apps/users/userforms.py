# encoding:utf-8
import re

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class UserRegisterForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={'invalid': u'邮箱地址非法'})
    password = forms.CharField(max_length=50, min_length=5, required=True,
                               error_messages={'min_length': u'密码长度少于5位'})
    captcha = CaptchaField(required=True, error_messages={'invalid': u'验证码错误'})


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={'invalid': u'邮箱地址非法'})
    captcha = CaptchaField(required=True, error_messages={'invalid': u'验证码错误'})


class ResetForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5, max_length=20, error_messages={
        'min_length': u'密码长度少于5位',
        'max_length': u'密码长度大于20位'
    })
    password2 = forms.CharField(required=True, min_length=5, max_length=20, error_messages={
        'min_length': u'密码长度少于5位',
        'max_length': u'密码长度大于20位'
    })


class UserImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoModifyForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'birthday', 'gender', 'address', 'cell_number']

    def clean_cell_number(self):
        reg = r'^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$'
        cell_number = self.cleaned_data['cell_number']
        if re.match(reg, cell_number):
            return cell_number
        else:
            raise forms.ValidationError(u'电话号码错误', code='phone_error')



