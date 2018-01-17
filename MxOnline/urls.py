# encoding:utf-8
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from MxOnline.settings import MEDIA_ROOT
from users.views import UserLoginView, UserRegisterView, UserActivate, ForgetPasswordView, UserResetView, user_logout
# from users.views import test_ajax, test_ajax2


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^login/$', UserLoginView.as_view(), name='user_login'),
    url(r'^logout/$', user_logout, name='user_logout'),
    url(r'^register/$', UserRegisterView.as_view(), name='user_register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^activate/(?P<activate_code>\w+)$', UserActivate.as_view(), name='user_activate'),
    url(r'^forget/$', ForgetPasswordView.as_view(), name='forget_password'),
    url(r'^reset/(?P<activate_code>\w+)$', UserResetView.as_view(), name='user_reset'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),  # media url 路由
    # url(r'^test_ajax/$', test_ajax, name='test_ajax'),
    # url(r'^test_ajax2/$', test_ajax2, name='test_ajax2'),
    url(r'^user/', include('users.urls', namespace='user')),
    url(r'^org/', include('organization.urls', namespace='org')),
    url(r'^course/', include('course.urls', namespace='course')),
    url(r'^operation/', include('operation.urls', namespace='operation')),

    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),  # static url
]


handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
