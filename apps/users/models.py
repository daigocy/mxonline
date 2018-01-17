# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    nickname = models.CharField(
        max_length=20, null=True, blank=True, default='', verbose_name=u'昵称')
    birthday = models.DateField(null=True, blank=True, verbose_name=u'生日')
    gender = models.CharField(
        choices=(('male', u'男'), ('female', u'女')),
        max_length=6, null=True, blank=True, default='male', verbose_name=u'性别'
    )
    cell_number = models.CharField(max_length=11, null=True, blank=True, verbose_name=u'电话')
    address = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=u'住址')
    image = models.ImageField(
        max_length=50, upload_to='user_image/', default=u'user_image/default.jpg')

    class Meta:
        verbose_name = u'用户表'
        verbose_name_plural = verbose_name


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(
        choices=(('register', u'注册'), ('forget', u'忘记密码'), ('modify', u'更换邮箱')),
        max_length=10, default='register', verbose_name=u'发送类型'
    )
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(upload_to="banner/%Y/%m/", verbose_name=u'图片')
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    index = models.IntegerField(default=100, verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name
