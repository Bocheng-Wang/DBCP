from django.urls import path, include

from . import views

urlpatterns = [
    path('ProjectDescription', views.ProjectDescription, name='ProjectDescription'),
    path('ProjectProgress', views.ProjectProgress, name='ProjectProgress'),
    path('ProjectMember', views.ProjectMember, name='ProjectCooperation'),
    path('ContactUs', views.ContactUs, name='ContactUs'),
    path('', views.homepage, name='homepage'),
]
