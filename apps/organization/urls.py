from django.conf.urls import url
# from django.views.generic import TemplateView

from .views import OrgListView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView
from .views import TeacherListView, TeacherHomeView


urlpatterns = [
    url(r'^org_list/$', OrgListView.as_view(), name='org_list'),
    url(r'^org_home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^org_course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^org_desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),
    url(r'^teacher_list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher_home/(?P<teacher_id>\d+)/$', TeacherHomeView.as_view(), name='teacher_home'),
    ]
