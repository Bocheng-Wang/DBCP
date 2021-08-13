from django.db import models

from UserManagement.models import User
import uuid


# Create your models here.





class Subject(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女')
    )
    subjectID = models.CharField(max_length=255, unique=True)
    career = models.CharField(max_length=255)
    education_years = models.IntegerField(default=0)
    sex = models.CharField(max_length=10, choices=gender)

    @classmethod
    def create(cls, subjectID):
        subject = cls(subjectID=subjectID)
        return subject


class Visit(models.Model):
    phase = (
        ('BL', '基线随访'),
        ('SC', '观察阶段'),
        ('M03', '三月随访'),
        ('M06', '半年随访'),
        ('M12', '一年随访'),
        ('M24', '两年随访'),
        ('M36', '三年随访'),
        ('M48', '四年随访'),
        ('M60', '五年随访')
    )

    diagnosis = (
        ('Healthy Control', '健康对照'),
        ('Early MCI', '早期轻度认知障碍'),
        ('Late MCI', '晚期轻度认知障碍'),
        ('Alzheimer`s Disease', '阿尔兹海默症')
    )

    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    Visit_age = models.FloatField(default=0)
    Phase = models.CharField(max_length=50, choices=phase)
    Diagnosis = models.CharField(max_length=50, choices=diagnosis)
    visit_time = models.DateTimeField(null=True, blank=True)
    MMSE = models.FloatField(default=0)
    CDR = models.FloatField(default=0)

    @classmethod
    def create(cls, subject, visit_age, Phase, Diagnosis):
        visit = cls(Subject=subject, Visit_age=visit_age, Phase=Phase, Diagnosis=Diagnosis)
        return visit


# in fact, we only accept .zip file here. Coding with mistake BC.Wang, 2020.09
class RARFile(models.Model):
    filename = models.CharField(max_length=255)
    filesize = models.IntegerField(default=0)
    storage_path = models.CharField(max_length=255)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    isCheck = models.BooleanField(default=False)

    @classmethod
    def create(cls, uploader, upload_time, filename, filesize, storage_path):
        zip = cls(upload_time=upload_time, uploader=uploader, filename=filename, filesize=filesize,
                  storage_path=storage_path)
        return zip

    def __str__(self):
        return self.filename


class ModalInfo(models.Model):
    modal = (
        ('MRI', "磁共振"),
        ('DTI', "扩散张量成像"),
        ('Fieldmap', "场域信息"),
    )

    source = (
        ('ADNI1', 'ADNI1',),
        ('ADNI2', 'ADNI2'),
        ('ADNI3', 'ADNI3'),
        ('ADNI_GO', 'ADNI_GO'),
    )

    uuidStr = models.CharField(max_length=50, default=str(uuid.uuid4()))
    modalName = models.CharField(max_length=50, choices=modal)
    DataSource = models.CharField(max_length=100, choices=source)

    Visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    RARFile = models.ForeignKey(RARFile, on_delete=models.SET_NULL, null=True)
    OtherFilePath = models.CharField(max_length=255)

    @classmethod
    def create(cls, modalName, DataSource, Visit, RARFile, UUID):
        modal = cls(modalName=modalName, DataSource=DataSource, Visit=Visit, RARFile=RARFile, uuidStr = UUID)
        return modal


# class Server(models.Model):
#     Server_Name = models.CharField(max_length=50, null=True)
#     Server_IP = models.CharField(max_length=20, default='0.0.0.0')
#     Server_IsBusy = models.BooleanField(default=False)
#
#
# class PreprocessTask(models.Model):
#     Task_Modal = models.ForeignKey(ModalInfo, on_delete=models.CASCADE, null=True)
#     Task_Server = models.ForeignKey(Server, on_delete=models.SET_NULL, null=True)
#     Task_Start = models.BooleanField(default=False)
#     Task_StartTime = models.DateTimeField(null=True, blank=True)
#     Task_Finish = models.BooleanField(default=False)
#     Task_EndTime = models.DateTimeField(null=True, blank=True)
#     Preprocess_Type = models.CharField(max_length=10, null=True)
#     Preprocessed_Dir = models.CharField(max_length=255, null=True)
#     AfterPreprocessed_Saved_Dir = models.CharField(max_length=255, null=True)
#     Progress_value = models.FloatField(default=0)
#     Task_Thread_ID = models.IntegerField(default=0)


class Connectivity(models.Model):
    mode = (
        ('static', '静态'),
        ('dynamic', '动态'),
    )
    Mode = models.CharField(max_length=10, choices=mode)
    generate_time = models.DateTimeField(auto_now_add=True)
    frameNumInDynamic = models.IntegerField(default=0)
