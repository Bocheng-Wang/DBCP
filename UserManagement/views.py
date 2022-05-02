import datetime
from email.mime.image import MIMEImage

import pytz

from ContentManagement import VisitStatistic

utc = pytz.UTC
from django import forms
from django.shortcuts import render, redirect

from DBCP import settings
from UserManagement import models

from django.http import JsonResponse
from UserManagement.forms import UserForm, RegisterForm
from UserManagement import Toolbox
from captcha.models import CaptchaStore
from django.utils import timezone
from django.utils.translation import gettext as _


def userdetail(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    if request.session.get('is_login', None):
        return render(request, 'UserManagement/userdetail.html', locals())
    return redirect("/", {"currentIP": currentIP, 'total_visit': totalVisit})


def captcha_ajax_val(request):
    if request.is_ajax():
        cs = CaptchaStore.objects.filter(response=request.GET['response'], hashkey=request.GET['hashkey'])
        if cs:
            json_data = {'status': 0}
        else:
            json_data = {'status': 1}
        return JsonResponse(json_data)
    else:
        # raise Http404
        json_data = {'status': 0}
        return JsonResponse(json_data)


def login(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    if request.session.get('is_login', None):
        return redirect("/")

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = _('Please re-check the contents filled')
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if not user.has_confirmed:
                    message = _("Please wait for the approval of website`s manager")
                    return render(request, 'UserManagement/login.html',
                                  {'message': message, 'login_form': login_form, "currentIP": currentIP,
                                   'total_visit': totalVisit})
                if user.password == Toolbox.hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/DBCPOnline/Preparation', {"currentIP": currentIP,
                                                                'total_visit': totalVisit})
                else:
                    message = _("Incorrect username or password!")
            except:
                message = _("Incorrect username or password!")
        return render(request, 'UserManagement/login.html',
                      {"message": message, 'login_form': login_form, "currentIP": currentIP,
                       'total_visit': totalVisit})
    login_form = UserForm()
    return render(request, 'UserManagement/login.html', {'login_form': login_form, "currentIP": currentIP,
                                                         'total_visit': totalVisit})


def register(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":

        register_form = RegisterForm(request.POST)
        message = _('Please re-check the contents filled')
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            # sex = register_form.cleaned_data['sex']
            usage = register_form.cleaned_data['usage']
            affiliation = register_form.cleaned_data['affiliation']
            if password1 != password2:
                message = _("Passwords filled not match")
                return render(request, 'UserManagement/register.html',
                              {'message': message, 'register_form': register_form, "currentIP": currentIP,
                               'total_visit': totalVisit})
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = _('UserName existed !')
                    return render(request, 'UserManagement/register.html',
                                  {'message': message, 'register_form': register_form, "currentIP": currentIP,
                                   'total_visit': totalVisit})
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = _('Email address occupied !')
                    return render(request, 'UserManagement/register.html',
                                  {'message': message, 'register_form': register_form, "currentIP": currentIP,
                                   'total_visit': totalVisit})

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = Toolbox.hash_code(password1)
                new_user.email = email
                # new_user.sex = sex
                new_user.usage = usage
                new_user.affiliation = affiliation
                new_user.save()

                code = Toolbox.Make_ConfirmString(new_user)
                try:
                    Toolbox.SendUserConfirmMail(new_user.name, email, code)
                except:
                    return redirect('/UserManagement/login/',
                                    {"currentIP": currentIP, 'total_visit': totalVisit})  # 自动跳转到登录页面
                return redirect('/UserManagement/login/',
                                {"currentIP": currentIP, 'total_visit': totalVisit})  # 自动跳转到登录页面
        return render(request, 'UserManagement/register.html',
                      {'message': message, 'register_form': register_form, "currentIP": currentIP,
                       'total_visit': totalVisit})
    register_form = RegisterForm()
    return render(request, 'UserManagement/register.html',
                  {'register_form': register_form, "currentIP": currentIP, 'total_visit': totalVisit})


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")

    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/")


# 用户发送注册请求后，点击确认按钮，后台给管理员发审核信息
def confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = _('Invalid request or the confirm link has been expired !')
        return render(request, 'UserManagement/confirm.html', {'message': message})

    c_time = confirm.c_time
    c_time = c_time.replace(tzinfo=utc)
    now = timezone.now()
    day_limit = c_time + datetime.timedelta(days=settings.CONFIRM_DAYS)
    day_limit = day_limit.replace(tzinfo=utc)
    if now > day_limit:
        confirm.user.delete()
        message = _('The link has been expired. Please re-registration')
        return render(request, 'UserManagement/confirm.html', locals())
    else:
        Toolbox.ManagerConfirmMail(confirm.user, code)
        # confirm.user.has_confirmed = True
        # confirm.user.save()
        # confirm.delete()
        message = _('Succeed! Please wait for the final approval backend')
        return render(request, 'UserManagement/confirm.html', locals())


# 管理员对新申请注册用户的审核
def Manager_confirm(request):
    code = request.GET.get('code', None)
    result = request.GET.get('result', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = _('Invalid Request')
        return render(request, 'UserManagement/confirm.html', {'message': message})
    if result == 'active':
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = _('The request has been approved')
        return render(request, 'UserManagement/confirm.html', locals())
    elif result == 'inactive':
        confirm.delete()
        confirm.user.delete()
        message = _('The request has been canceled')
        return render(request, 'UserManagement/confirm.html', locals())
