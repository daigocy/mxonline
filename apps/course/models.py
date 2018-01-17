# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'名称')
    desc = models.CharField(max_length=300, verbose_name=u'描述')
    detail = models.TextField(verbose_name=u'详情')
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构', default='1')
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师')
    degree = models.CharField(
        choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')),
        default='cj', max_length=2, verbose_name=u'难度'
    )
    learn_time = models.IntegerField(default=0, verbose_name=u'时长（分钟）')
    image = models.ImageField(upload_to='courses/%Y/%m/', verbose_name=u'图片', max_length=100)
    category = models.CharField(max_length=50, verbose_name=u'类别')
    student_num = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_num = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_num = models.IntegerField(default=0, verbose_name=u'点击人数')
    you_need_know = models.CharField(max_length=300, verbose_name=u'课前准备', default='')
    course_teach_you = models.CharField(max_length=300, verbose_name=u'学到知识', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_num(self):
        return self.lesson_set.count()

    def get_learning_users(self):
        return self.usercourse_set.all()[:5]

    # def get_learning_num(self):
    #     return self.usercourse_set.count()

    def get_lessons(self):
        return self.lesson_set.all()

    def get_resources(self):
        return self.courseresource_set.all()

    def get_learn_time(self):
        time = 0
        for lesson in self.lesson_set.all():
            time += lesson.get_lean_time()
        return time


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'所属课程')
    desc = models.CharField(max_length=300, verbose_name=u'描述', default=u'暂无描述')
    name = models.CharField(max_length=50, verbose_name=u'名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_videos(self):
        return self.video_set.all()

    def get_lean_time(self):
        time = 0
        for video in self.video_set.all():
            time += video.learn_time
        return time


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'所属章节')
    name = models.CharField(max_length=50, verbose_name=u'名称')
    learn_time = models.IntegerField(default=0, verbose_name=u'时长（分钟）')
    path = models.CharField(max_length=200, default='', verbose_name=u'MP4路径')
    path2 = models.CharField(max_length=200, default='', verbose_name=u'OGG路径')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'所属课程')
    name = models.CharField(max_length=50, verbose_name=u'名称')
    download = models.FileField(
        upload_to='resource/%Y/%m/',
        verbose_name=u'路径', max_length=100
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
