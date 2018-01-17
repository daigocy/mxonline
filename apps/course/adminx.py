# encoding:utf-8
import xadmin

from .models import Course, Lesson, Video, CourseResource


class CourseXadmin(object):
    list_display = ['name', 'desc', 'degree', 'course_org']
    list_filter = ['name', 'desc', 'degree', 'course_org']
    search_fields = ['name', 'desc', 'degree', 'course_org__name']


class LessonXadmin(object):
    list_display = ['name', 'desc', 'course']
    list_filter = ['name', 'desc', 'course']
    search_fields = ['name', 'desc', 'course__name']


class VideoXadmin(object):
    list_display = ['name', 'lesson']
    list_filter = ['name', 'lesson']
    search_fields = ['name', 'lesson__name']


class CourseResourceXadmin(object):
    list_display = ['name', 'course']
    list_filter = ['name', 'course']
    search_fields = ['name', 'course__name']

xadmin.site.register(Course, CourseXadmin)
xadmin.site.register(Lesson, LessonXadmin)
xadmin.site.register(Video, VideoXadmin)
xadmin.site.register(CourseResource, CourseResourceXadmin)
