# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from users.models import UserProfile
from course.models import Course


# Create your models here.
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    phone_num = models.CharField(max_length=11, verbose_name=u'手机')
    course_ask = models.CharField(max_length=20, verbose_name=u'咨询课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name


class UserComment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    comment = models.CharField(max_length=200, verbose_name=u'用户评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'评论时间')

    class Meta:
        verbose_name = u'用户评论'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    fav_id = models.IntegerField(default=0, verbose_name=u'对象id')
    fav_type = models.IntegerField(
        choices=((1, u'课程'), (2, u'机构'), (3, u'讲师')),
        default=1,
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'收藏时间')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u'接受用户')
    message = models.CharField(max_length=200, verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'订阅时间')

    class Meta:
        verbose_name = u'课程订阅'
        verbose_name_plural = verbose_name
