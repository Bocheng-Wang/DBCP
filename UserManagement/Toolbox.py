import datetime
import hashlib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.mail import EmailMultiAlternatives
from django.template import loader
from email.mime.image import MIMEImage
from UserManagement import models
from DBCP import settings
from django.utils.translation import gettext as _

os.environ['DJANGO_SETTINGS_MODULE'] = 'DBCP.settings'


# def add_img(src, img_id):
#     with open(src, 'rb') as f:
#         msg_image = MIMEImage(f.read())
#     msg_image.add_header('Content-ID', img_id)
#     return msg_image

# 管理员审核注册用户信息
def ManagerConfirmMail(user, code):
    subject, from_email, to = 'DBCP-Online Registration', settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER
    result = ''

    activate_url = "http://{}/Manager_confirm/?result={}&code={}".format(
        settings.CUSTOM_SETTINGS['Domain'] + '/UserManagement', 'active', code)
    in_activate_url = "http://{}/Manager_confirm/?result={}&code={}".format(
        settings.CUSTOM_SETTINGS['Domain'] + '/UserManagement', 'inactive', code)
    context = {
        'user_name': user.name,
        'email_addr': user.email,
        'affiliation': user.affiliation,

        'usage': user.usage,
        'active_url': activate_url,
        'in_active_url': in_activate_url,
    }
    email_template_name = 'manager_confirm_email_template.html'
    t = loader.get_template(email_template_name)
    html_content = t.render(context)
    text_content = "信息审核： " + context['active_url']
    file_path = settings.STATICFILES_DIRS[0] + '\\Images\\brain.png'
    # image = add_img(file_path, 'brainPNG')

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach(image)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# 给注册用户发送确认连接
def SendUserConfirmMail(user_name, email, code):
    subject, from_email, to = 'DBCP-Online Registration', settings.EMAIL_HOST_USER, email
    href = "http://{}/confirm/?code={}".format(settings.CUSTOM_SETTINGS['Domain'] + '/UserManagement', code)
    context = {
        'user_name': user_name,
        'active_url': href,
    }
    email_template_name = 'user_confirm_email_template.html'
    t = loader.get_template(email_template_name)
    html_content = t.render(context)
    text_content = _('Click here to confirm your address') + context['active_url']
    file_path = settings.STATICFILES_DIRS[0] + '\\Images\\brain.png'
    # image = add_img(file_path, 'brainPNG')

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach(image)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def Make_ConfirmString(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code
