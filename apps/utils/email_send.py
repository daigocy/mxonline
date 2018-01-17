# encoding:utf-8
from random import Random

from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


def send_link_email(email, send_type='register'):
    record = EmailVerifyRecord()
    record.email = email
    record.send_type = send_type
    if send_type == 'modify':
        record.code = generate_code(4)
    else:
        record.code = generate_code(16)
    record.save()
    if send_type == 'register':
        email_title = '慕学网注册链接'
        email_body = '慕学网注册激活链接：http://127.0.0.1/activate/{0}'.format(record.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        return send_status
    if send_type == 'reset':
        email_title = '慕学网找回密码链接'
        email_body = '慕学网找回密码链接：http://127.0.0.1/reset/{0}'.format(record.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        return send_status
    if send_type == 'modify':
        email_title = '慕学网更换邮箱验证码'
        email_body = '验证码：{0} '.format(record.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        return send_status


def generate_code(code_length=4):
    code = ''
    codes = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    code_range = len(codes) - 1
    rand = Random()
    for i in range(code_length):
        code += codes[rand.randint(0, code_range)]
    return code
