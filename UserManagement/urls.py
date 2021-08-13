from django.urls import path, include

from . import views

urlpatterns = [

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('captcha/', include('captcha.urls')),
    path('confirm/', views.confirm, name='confirm'),
    path('Manager_confirm/', views.Manager_confirm, name='Manager_confirm'),
    path('captcha_ajax_val/', views.captcha_ajax_val, name='captcha_ajax_val'),  # 新加入
    path('userdetail/', views.userdetail, name='userdetail'),  # 新加入
]
