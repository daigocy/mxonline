# encoding:utf-8
from django.shortcuts import render
from django.http.response import HttpResponse

from .form import UserAskForm
from .models import UserFavorite, UserComment
from course.models import Course
from organization.models import CourseOrg, Teacher
# Create your views here.


def add_ask(request):
    user_ask = UserAskForm(request.POST)
    if user_ask.is_valid():
        user_ask.save(commit=True)
        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponse('{"status":"fail","msg":"输入信息错误"}', content_type='application/json')


def add_fav(request):
    if not request.user.is_authenticated():
        return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
    fav_id = int(request.POST.get('fav_id', 0))
    fav_type = int(request.POST.get('fav_type', 0))
    record_existed = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
    if record_existed:
        if fav_type == 1:
            course = Course.objects.get(id=fav_id)
            if course.fav_num:
                course.fav_num -= 1
                course.save()
        if fav_type == 2:
            org = CourseOrg.objects.get(id=fav_id)
            if org.fav_num:
                org.fav_num -= 1
                org.save()
        if fav_type == 3:
            teacher = Teacher.objects.get(id=fav_id)
            if teacher.fav_num:
                teacher.fav_num -= 1
                teacher.save()
        record_existed.delete()
        return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
    if fav_id > 0 and fav_type > 0:
        if fav_type == 1:
            course = Course.objects.get(id=fav_id)
            course.fav_num += 1
            course.save()
        if fav_type == 2:
            org = CourseOrg.objects.get(id=fav_id)
            org.fav_num += 1
            org.save()
        if fav_type == 3:
            teacher = Teacher.objects.get(id=fav_id)
            teacher.fav_num += 1
            teacher.save()
        user_fav = UserFavorite()
        user_fav.fav_id = fav_id
        user_fav.fav_type = fav_type
        user_fav.user = request.user
        user_fav.save()
        return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
    else:
        return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


def add_comment(request):
    if not request.user.is_authenticated():
        return HttpResponse('{"status":"fail","msg":"请先登录"}', content_type='application/json')
    course_id = int(request.POST.get('course_id', 0))
    comments = request.POST.get('comments', '')
    try:
        course = Course.objects.get(id=course_id)
        user_comment = UserComment()
        user_comment.course = course
        user_comment.user = request.user
        user_comment.comment = comments
        user_comment.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')
    except Exception as e:
        return HttpResponse('{"status":"fail","msg":"课程出错"}', content_type='application/json')


