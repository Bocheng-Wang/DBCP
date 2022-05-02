from django.urls import path, include

from . import views

urlpatterns = [
    path('SuccessOnRemoteCompute/<str:UUID>', views.SuccessOnRemoteCompute, name='SuccessOnRemoteCompute'),
    path('FailInRemoteCompute/<str:UUID>', views.FailInRemoteCompute, name='FailInRemoteCompute'),
    path('CheckTasks/<str:range>', views.CheckTasks, name='CheckTasks'),
    path('ResetPreprocessingTask/<str:ModalID>', views.ResetPreprocessingTask, name='ResetPreprocessingTask'),
    path('getConnectivityFiles/<str:ModalID>', views.getConnectivityFiles, name='getConnectivityFiles'),
]
