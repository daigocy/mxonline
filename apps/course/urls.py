# encoding:utf-8
from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseVideo, CourseComment, VideoPlay


urlpatterns = [
    url(r'^course_list/$', CourseListView.as_view(), name='course_list'),
    url(r'^course_detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^course_video/(?P<course_id>\d+)/$', CourseVideo.as_view(), name='course_video'),
    url(r'^course_comment/(?P<course_id>\d+)/$', CourseComment.as_view(), name='course_comment'),
    url(r'^video_play/(?P<video_id>\d+)/$', VideoPlay.as_view(), name='video_play'),
]
