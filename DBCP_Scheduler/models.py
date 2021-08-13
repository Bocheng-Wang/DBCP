from django.db import models

from DBCPOnline.models import ModalInfo


class Server(models.Model):
    Server_Name = models.CharField(max_length=50, null=True)
    Server_IP = models.CharField(max_length=20, default='0.0.0.0')
    Server_IsBusy = models.BooleanField(default=False)
    # Server_IsParcellation_and_CorrelationBusy = models.BooleanField(default=False)
    Server_Type = models.CharField(max_length=50, null=True)


class TaskQueue(models.Model):
    Type = models.CharField(max_length=50, null=True)
    # NeedThreading = models.BooleanField(default=True)
    isScheduled = models.BooleanField(default=True)
    Description = models.CharField(max_length=150, null=True)
    isDebug = models.BooleanField(default=True)
    Task_LastRunTime = models.DateTimeField(null=True, blank=True)

class CorrelationConnectivityTask(models.Model):
    Task_Modal = models.ForeignKey(ModalInfo, on_delete=models.CASCADE, null=True)
    Task_Server = models.ForeignKey(Server, on_delete=models.SET_NULL, null=True)
    Task_Start = models.BooleanField(default=False)
    Task_StartTime = models.DateTimeField(null=True, blank=True)
    Task_Finish = models.BooleanField(default=False)
    Task_EndTime = models.DateTimeField(null=True, blank=True)
    Preprocess_Type = models.CharField(max_length=10, null=True)
    Preprocessed_Dir = models.CharField(max_length=255, null=True)
    AfterPreprocessed_Saved_Dir = models.CharField(max_length=255, null=True)
    Progress_value = models.FloatField(default=0)
    Task_Thread_ID = models.IntegerField(default=0)
    Task_Status = models.IntegerField(default=200)


class CausalityConnectivityTask(models.Model):
    Task_Modal = models.OneToOneField(ModalInfo, on_delete=models.CASCADE, null=True, unique=True)
    Task_Server = models.ForeignKey(Server, on_delete=models.SET_NULL, null=True)
    Task_Start = models.BooleanField(default=False)
    Task_StartTime = models.DateTimeField(null=True, blank=True)
    Task_Finish = models.BooleanField(default=False)
    Task_EndTime = models.DateTimeField(null=True, blank=True)
    Task_Type = models.CharField(max_length=50, null=True)
    Preprocessed_Dir = models.CharField(max_length=255, null=True)
    AfterPreprocessed_Saved_Dir = models.CharField(max_length=255, null=True)
    Progress_value = models.FloatField(default=0)
    Task_Thread_ID = models.IntegerField(default=0)
    Task_Status = models.IntegerField(default=200)
