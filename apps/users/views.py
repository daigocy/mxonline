# encoding:utf-8
import json
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http.response import HttpResponseRedirect, HttpResponse

from pure_pagination import Paginator, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord
from .userforms import UserRegisterForm, ForgetPasswordForm, ResetForm, UserImageUploadForm, UserInfoModifyForm
from operation.models import UserCourse, UserFavorite
from utils.email_send import send_link_email
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.
class UserAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserLoginView(View):
    def get(self, request):
        next_page = request.GET.get('next', '')
        return render(request, 'login.html', {'next_page': next_page})

    def post(self, request):
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        next_page = request.POST.get('next', '')
        user = authenticate(username=user_name, password=pass_word)
        if user:
            if user.is_active:
                login(request, user)
                if not next_page:
                    return render(request, 'index.html')
                return HttpResponseRedirect(next_page)
            else:
                return render(request, 'login.html', {
                     'error_msg': '用户未激活',
                     'user_name': user_name,
                     'pass_word': pass_word,
                     # 'next_page': next_page,
                 })
        else:
            return render(request, 'login.html', {
                'error_msg': '认证失败',
                'user_name': user_name,
                'pass_word': pass_word,
                # 'next_page': next_page,
            })


class UserRegisterView(View):
    def get(self, request):
        register_form = UserRegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            user_email = request.POST.get('email', '')
            user_password = request.POST.get('password', '')
            test_exist = UserProfile.objects.filter(email=user_email)
            if test_exist and test_exist[0].is_active:
                    return render(request, 'register.html', {'register_form': register_form, 'exist': u'邮箱已注册'})
            user = UserProfile()
            user.username = user_email
            user.email = user_email
            user.password = make_password(user_password)
            user.is_active = False
            send_status = send_link_email(user_email, send_type='register')
            if send_status:
                user.save()
                return render(request, 'login.html', {
                    'error_msg': '已发送激活链接至邮件，请激活后登陆',
                    'user_name': user_email,
                    'pass_word': user_password,
                })
            else:
                return render(request, 'register.html', {'register_form': register_form, 'exist': '邮件发送失败'})
        else:
            return render(request, 'register.html', {'register_form': register_form})


class UserActivate(View):
    def get(self, request, activate_code):
        user_emails = EmailVerifyRecord.objects.filter(code=activate_code)
        user = UserProfile.objects.get(email=user_emails[0].email)
        user.is_active = True
        user.save()
        return render(request, 'login.html')


class ForgetPasswordView(View):
    def get(self, request):
        forget_from = ForgetPasswordForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_from})

    def post(self, request):
        forget_from = ForgetPasswordForm(request.POST)
        if forget_from.is_valid():
            email = request.POST.get('email')
            user = UserProfile.objects.filter(email=email)
            if user:
                send_status = send_link_email(email, send_type='forget')
                if send_status:
                    pass
                return render(request, 'forgetpwd.html', {'forget_form': forget_from, 'no_exist': '邮件已发送'})
            else:
                return render(request, 'forgetpwd.html', {'forget_form': forget_from, 'no_exist': '用户不存在'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_from})


class UserResetView(View):
    def get(self, request, activate_code):
        user_emails = EmailVerifyRecord.objects.filter(code=activate_code)
        user = UserProfile.objects.get(email=user_emails[0].email)
        return render(request, 'password_reset.html', {'user': user})

    def post(self, request, activate_code):
        user_id = request.POST.get('user_id')
        user = UserProfile.objects.get(id=int(user_id))
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user.password = make_password(password1)
                user.save()
                return render(request, 'password_reset.html', {'user': user, 'msg': '修改成功'})
            else:
                return render(request, 'password_reset.html', {'user': user, 'msg': '两次密码不同'})
        else:
            return render(request, 'password_reset.html', {'user': user, 'reset_form': reset_form})


def user_logout(request):  # 临时退出函数
    logout(request)
    return render(request, 'index.html')

''' 测试AJAX
def test_ajax(request):
    return HttpResponse("ajax request :test django-ajax", content_type="application/json")


def test_ajax2(request):
    return render(request, 'test1.html')
'''


class UserHomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        info_form = UserInfoModifyForm(request.POST, instance=request.user)
        if info_form.is_valid():
            info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(info_form.errors), content_type='application/json')


class UserImageUploadView(LoginRequiredMixin, View):
    def post(self, request):
        upload_form = UserImageUploadForm(request.POST, request.FILES, instance=request.user)
        if upload_form.is_valid():
            upload_form.save()


class UserPwdModifyView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user.password = make_password(password1)
                user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"两次输入密码不一致"}', content_type='application/json')
        else:
            x = json.dumps(reset_form.errors)
            return HttpResponse(x, content_type='application/json')


class UserEmailModifyView(LoginRequiredMixin, View):
    def get(self, request):
        mail = request.GET.get('email', '')
        if UserProfile.objects.filter(email=mail):
            return HttpResponse('{"email":"邮箱已注册"}', content_type='application/json')
        send_status = send_link_email(email=mail, send_type='modify')
        if send_status:
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failure"}', content_type='application/json')

    def post(self, request):
        mail = request.POST.get('email', '')
        if UserProfile.objects.filter(email=mail):
            return HttpResponse('{"email":"邮箱已注册"}', content_type='application/json')
        code = request.POST.get('code', '')
        if not code:
            return HttpResponse('{"code":"验证码为空"}', content_type='application/json')
        else:
            if EmailVerifyRecord.objects.filter(email=mail, code=code, send_type='modify'):
                user = request.user
                user.email = mail
                user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"code":"验证码错误"}', content_type='application/json')


class UserCourseLeanedView(LoginRequiredMixin, View):
    def get(self, request):
        my_courses = [user_course.course for user_course in UserCourse.objects.filter(user=request.user)]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(my_courses, 8, request=request)  # request的传入是为了保留其他get参数
        my_courses_per_page = p.page(page)
        fav_course_ids = [fav_record.fav_id for fav_record in UserFavorite.objects.filter(user=request.user, fav_type=1)]
        return render(request, 'usercenter-mycourse.html', {
            'my_courses': my_courses_per_page,
            'fav_course_ids': fav_course_ids,
        })


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response


def index(request):
    return render('index.html', {})
