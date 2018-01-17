# encoding:utf-8
from django.shortcuts import render
from django.views.generic import View
# from django.db.models import Q

from pure_pagination import Paginator, PageNotAnInteger

from .models import CourseOrg, City, Teacher
from operation.models import UserFavorite
# Create your views here.


class OrgListView(View):
    def get(self, request):
        ct = request.GET.get('ct', '')
        city_id = request.GET.get('city', '')
        sort_type = request.GET.get('sort', '')
        organizations = CourseOrg.objects.all()
        orglist_right = organizations.order_by('-student_num')[:3]
        # orglist_right = sorted(organizations, key=CourseOrg.count_student, reverse=True)[:3]
        if ct:
            organizations = organizations.filter(category=ct)
        if city_id:
            organizations = organizations.filter(city_id=int(city_id))
        if sort_type == 'courses':
            organizations = sorted(organizations, key=CourseOrg.count_course, reverse=True)
        elif sort_type == 'students':
            organizations = organizations.order_by('-student_num')
            # organizations = sorted(organizations, key=CourseOrg.count_student, reverse=True)
        org_num = len(organizations)
        cities = City.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(organizations, 5, request=request)  # request的传入是为了保留其他get参数
        org_per_page = p.page(page)
        return render(request, 'org_list.html', {
            'organizations': org_per_page,
            'cities': cities,
            'org_mun': org_num,
            'ct': ct,
            'city_id': city_id,
            'sort_type': sort_type,
            'orglist_right': orglist_right
        })


class OrgHomeView(View):
    def get(self, request, org_id):
        cu_page = 'org_home'
        has_fav = "收藏"
        fav_course_ids = []
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = '已收藏'
            fav_course_ids = [
                user_fav.fav_id for user_fav in UserFavorite.objects.filter(user=request.user, fav_type=1)]
        org = CourseOrg.objects.get(id=int(org_id))
        org.click_num += 1
        org.save()
        courses = org.course_set.all()[0:3]
        teachers = org.teacher_set.all()[0:3]
        return render(request, 'org-detail-homepage.html', {
            'cu_page': cu_page,
            'has_fav': has_fav,
            'fav_course_ids': fav_course_ids,
            'org': org,
            'courses': courses,
            'teachers': teachers,
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        cu_page = 'org_course'
        has_fav = "收藏"
        fav_course_ids = []
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = '已收藏'
            fav_course_ids = [
                user_fav.fav_id for user_fav in UserFavorite.objects.filter(user=request.user, fav_type=1)]
        org = CourseOrg.objects.get(id=int(org_id))
        courses = org.course_set.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(courses, 8, request=request)  # request的传入是为了保留其他get参数
        course_per_page = p.page(page)
        return render(request, 'org-detail-course.html', {
            'cu_page': cu_page,
            'has_fav': has_fav,
            'fav_course_ids': fav_course_ids,
            'org': org,
            'courses': course_per_page,
        })


class OrgDescView(View):
    def get(self, request, org_id):
        cu_page = 'org_desc'
        has_fav = "收藏"
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = '已收藏'
        org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {
            'cu_page': cu_page,
            'has_fav': has_fav,
            'org': org,
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        cu_page = 'teacher'
        has_fav = "收藏"
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = '已收藏'
        org = CourseOrg.objects.get(id=int(org_id))
        teachers = org.teacher_set.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, 5, request=request)  # request的传入是为了保留其他get参数
        teacher_per_page = p.page(page)
        return render(request, 'org-detail-teachers.html', {
            'cu_page': cu_page,
            'has_fav': has_fav,
            'org': org,
            'teachers': teacher_per_page,
        })


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all().order_by('-add_time')
        sorted_teachers = Teacher.objects.all().order_by('-click_mum')[:3]
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_mum')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 5, request=request)  # request的传入是为了保留其他get参数
        teachers_per_page = p.page(page)
        return render(request, 'teachers-list.html', {
            'sort': sort,
            'all_teachers': teachers_per_page,
            'sorted_teachers': sorted_teachers
        })


class TeacherHomeView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_mum += 1
        teacher.save()
        has_fav_teacher = "收藏"
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_teacher = '已收藏'
        has_fav_org = "收藏"
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = '已收藏'
        fav_course_ids = []
        if request.user.is_authenticated():
            fav_course_ids = [
                fav_course.fav_id for fav_course in UserFavorite.objects.filter(user=request.user, fav_type=1)]
        courses = teacher.course_set.all()
        sorted_teachers = Teacher.objects.all().order_by('-click_mum')[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(courses, 3, request=request)  # request的传入是为了保留其他get参数
        courses_per_page = p.page(page)
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'courses': courses_per_page,
            'sorted_teachers': sorted_teachers,
            'has_fav_teacher': has_fav_teacher,
            'has_fav_org': has_fav_org,
            'fav_course_ids': fav_course_ids
        })

