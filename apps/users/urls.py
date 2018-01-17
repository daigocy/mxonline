# encoding:utf-8
from django.conf.urls import url

from .views import UserHomeView, UserImageUploadView, UserEmailModifyView, UserCourseLeanedView
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^home/$', UserHomeView.as_view(), name='home'),
    url(r'^home/image/upload$', UserImageUploadView.as_view(), name='image_upload'),
    url(r'^home/pwd/modify$', UserEmailModifyView.as_view(), name='password_modify'),
    url(r'^my_course/$', UserCourseLeanedView.as_view(), name='my_course')
]
