"""DBCP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.templatetags import static
from django.urls import path, include
from django.views.generic import RedirectView

from ContentManagement import views
from DBCP import settings
from UserManagement import views as UserManagementViews
from TimingTask.views import *
from KalmanFilter.views import *
from DBCP_Scheduler.views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('index/', views.homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('UserManagement/', include('UserManagement.urls')),
    path('ContentManagement/', include('ContentManagement.urls')),
    path('DBCPOnline/', include('DBCPOnline.urls')),
    path('KalmanFilter/', include('KalmanFilter.urls')),
    path('DBCPScheduler/', include('DBCP_Scheduler.urls')),
    path('favicon.ico', RedirectView.as_view(url='static/Images/icon.png')),
    path('robots.txt', TemplateView.as_view(template_name='static/robots.txt', content_type='text/plain')),
]
