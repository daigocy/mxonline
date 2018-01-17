# encoding:utf-8
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, Video
from operation.models import UserFavorite, UserCourse, UserComment
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    def get(self, request):
        courses = Course.objects.all()
        hot_courses = courses.order_by('-click_num')[:3]
        fav_course_ids = []
        if request.user.is_authenticated():
            fav_course_ids = [
                fav_course.fav_id for fav_course in UserFavorite.objects.filter(user=request.user, fav_type=1)]
        sort_type = request.GET.get('sort', '')
        if sort_type:
            if sort_type == 'hot':
                courses = courses.order_by('-click_num')
            if sort_type == 'students':
                courses = courses.order_by('-student_num')
                # courses = sorted(courses, key=Course.get_learning_num, reverse=True)
        else:
            courses = courses.order_by('-add_time')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(courses, 6, request=request)  # request的传入是为了保留其他get参数
        course_per_page = p.page(page)
        return render(request, 'course-list.html', {
            'courses': course_per_page,
            'hot_courses': hot_courses,
            'sort_type': sort_type,
            'fav_course_ids': fav_course_ids
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()
        if request.user.is_authenticated():
            user_fav_courses = [x.fav_id for x in UserFavorite.objects.filter(user=request.user, fav_type=1)]
            user_fav_organization = [x.fav_id for x in UserFavorite.objects.filter(user=request.user, fav_type=2)]
        else:
            user_fav_courses = []
            user_fav_organization = []
        learn_students = [user_course.user.id for user_course in UserCourse.objects.filter(course=course)]
        learned_courses = [user_course.course.id for user_course in UserCourse.objects.filter(
            Q(user_id__in=learn_students) & ~Q(course_id=course.id)
        )]
        other_courses = Course.objects.filter(id__in=learned_courses).order_by("-click_num")
        if other_courses.count() > 3:
            other_courses = other_courses[:3]
        return render(request, 'course-detail.html', {
            'course': course,
            'other_courses': other_courses,
            'user_fav_courses': user_fav_courses,
            'user_fav_organization': user_fav_organization,
        })


class CourseVideo(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        if not UserCourse.objects.filter(Q(user=request.user) & Q(course=course)):
            org_joined_list = [user_course.course.course_org.id
                               for user_course in UserCourse.objects.filter(user=request.user)]
            if course.course_org.id not in org_joined_list:
                course.course_org.student_num += 1
                course.course_org.save()
            course.student_num += 1
            course.save()
            add_user_course = UserCourse()
            add_user_course.user = request.user
            add_user_course.course = course
            add_user_course.save()
        learn_students = [user_course.user.id for user_course in UserCourse.objects.filter(course=course)]
        learned_courses = [user_course.course.id for user_course in UserCourse.objects.filter(
            Q(user_id__in=learn_students) & ~Q(course_id=course.id)
        )]
        other_courses = Course.objects.filter(id__in=learned_courses).order_by("-click_num")
        if other_courses.count() > 3:
            other_courses = other_courses[:3]
        return render(request, 'course-video.html', {
            'course': course,
            'other_courses': other_courses,
        })


class CourseComment(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        if not UserCourse.objects.filter(Q(user=request.user) & Q(course=course)):
            org_joined_list = [user_course.course.course_org.id
                               for user_course in UserCourse.objects.filter(user=request.user)]
            if course.course_org.id not in org_joined_list:
                course.course_org.student_num += 1
                course.course_org.save()
            course.student_num += 1
            course.save()
            add_user_course = UserCourse()
            add_user_course.user = request.user
            add_user_course.course = course
            add_user_course.save()
        learn_students = [user_course.user.id for user_course in UserCourse.objects.filter(course=course)]
        learned_courses = [user_course.course.id for user_course in UserCourse.objects.filter(
            Q(user_id__in=learn_students) & ~Q(course_id=course.id)
        )]
        other_courses = Course.objects.filter(id__in=learned_courses).order_by("-click_num")
        if other_courses.count() > 3:
            other_courses = other_courses[:3]
        all_comments = UserComment.objects.filter(course=course).order_by("-add_time")
        try:
            page = request.GET.get('page', -1)
        except PageNotAnInteger:
            page = -1
        p = Paginator(all_comments, 10, request=request)  # request的传入是为了保留其他get参数
        comments_per_page = p.page(page)
        return render(request, 'course-comment.html', {
            'course': course,
            'other_courses': other_courses,
            'all_comments': comments_per_page,
        })


class VideoPlay(LoginRequiredMixin, View):
    def get(self, request, video_id):
        current_video = Video.objects.get(id=int(video_id))
        course = current_video.lesson.course
        if not UserCourse.objects.filter(Q(user=request.user) & Q(course=course)):
            add_user_course = UserCourse()
            add_user_course.user = request.user
            add_user_course.course = course
            add_user_course.save()
        learn_students = [user_course.user.id for user_course in UserCourse.objects.filter(course=course)]
        learned_courses = [user_course.course.id for user_course in UserCourse.objects.filter(
            Q(user_id__in=learn_students) & ~Q(course_id=course.id)
        )]
        other_courses = Course.objects.filter(id__in=learned_courses).order_by("-click_num")
        if other_courses.count() > 3:
            other_courses = other_courses[:3]
        return render(request, 'course-play.html', {
            'current_video': current_video,
            'course': course,
            'other_courses': other_courses,
        })
