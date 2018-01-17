# encoding:utf-8
from .models import CourseOrg, Teacher, City

import xadmin


class CityXadmin(object):
    list_display = ['name', 'description']
    list_filter = ['name', 'description']
    search_fields = ['name', 'description']


class CourseOrgXadmin(object):
    list_display = ['name', 'description', 'city']
    list_filter = ['name', 'description', 'city']
    search_fields = ['name', 'description', 'city__name']


class TeacherXadmin(object):
    list_display = ['name', 'work_years', 'org']
    list_filter = ['name', 'work_years', 'org']
    search_fields = ['name', 'work_years', 'org__name']


xadmin.site.register(CourseOrg, CourseOrgXadmin)
xadmin.site.register(City, CityXadmin)
xadmin.site.register(Teacher, TeacherXadmin)
