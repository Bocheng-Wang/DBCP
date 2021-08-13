from django.urls import path, include

from . import views

urlpatterns = [
    path('ServerSchedulerSwitch/<str:type>/<str:switch>', views.ServerSchedulerSwitch, name='ServerSchedulerSwitch'),
    path('DebugSwitch/<str:type>/<str:switch>', views.DebugSwitch, name='DebugSwitch'),
]
