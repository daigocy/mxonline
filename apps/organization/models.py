# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'城市')
    description = models.CharField(max_length=200, verbose_name=u'描述')
    add_time = models.DateField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'机构名称')
    description = models.TextField(max_length=200, verbose_name=u'描述')
    category = models.CharField(max_length=4, choices={
        ('pxjg', u'培训机构'), ('gr', u'个人'), ('gx', u'高校')}, default='pxjg')
    image = models.ImageField(upload_to='org/%Y/%m/', verbose_name=u'封面')
    address = models.CharField(max_length=150, verbose_name=u'地址')
    city = models.ForeignKey(City, verbose_name=u'所在城市')
    click_num = models.IntegerField(default=0, verbose_name=u'点击量')
    fav_num = models.IntegerField(default=0, verbose_name=u'收藏量')
    student_num = models.IntegerField(default=0, verbose_name=u'学习人数')
    add_time = models.DateField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def count_course(self):
        return self.course_set.count()

    def count_teacher(self):
        return self.teacher_set.count()

    # def count_student(self):
    #     num = 0
    #     for course in self.course_set.all():
    #         num += course.get_learning_num()
    #     return num

    def get_hot_courses(self):
        hot_courses = self.course_set.all().order_by('-click_num')
        if hot_courses.count() > 2:
            hot_courses = hot_courses[:2]
        return hot_courses


class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'姓名')
    age = models.IntegerField(default=26, verbose_name=u'年龄')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'公司')
    work_position = models.CharField(max_length=50, verbose_name=u'职位')
    points = models.CharField(max_length=50, verbose_name=u'特点')
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构')
    click_mum = models.IntegerField(default=0, verbose_name=u'点击量')
    fav_mun = models.IntegerField(default=0, verbose_name=u'收藏量')
    add_time = models.DateField(default=datetime.now, verbose_name=u'添加时间')
    image = models.ImageField(upload_to='teacher/%Y/%m/', verbose_name=u'封面', default='teacher/default.jpg')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def count_courses(self):
        return self.course_set.count()
