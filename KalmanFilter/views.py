from DBCP_Scheduler.CausalityConnectivityPreprocessing import AbandonTask
from DBCP_Scheduler.models import CausalityConnectivityTask, TaskQueue
import base64
import os
import datetime
import json
import tempfile
import threading
import uuid
import zipfile
from wsgiref.util import FileWrapper

from apscheduler.schedulers.background import BackgroundScheduler
from django.core import serializers

from django.utils import timezone
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.conf import settings

# Create your views here.
from ContentManagement import VisitStatistic
from DBCPOnline import SSHCommand
from DBCPOnline.models import RARFile, Subject, Visit, ModalInfo
from DBCP_Scheduler import ServerManagement
from DBCP_Scheduler.models import CorrelationConnectivityTask, CausalityConnectivityTask, Server
from UserManagement.models import User

from django.http import FileResponse
import scipy.io as scio

import seaborn as sns
from matplotlib import pyplot


def SuccessOnRemoteCompute(request, UUID):
    return HttpResponse('Success    ' + UUID)


def FailInRemoteCompute(request, UUID):
    AbandonTask(ModalInfo.objects.get(uuidStr=UUID))
    return HttpResponse('Fali in    ' + UUID)


def getConnectivityFiles(request, ModalID):
    '''
    ?? Kalman ?????????
    :param request:
    :param ModalID:
    :return:
    '''

    def file_iterator(file, chunk_size=512):
        """
        ?????,?????????????
        :param file_path: ??????
        :param chunk_size: ???
        :return: ???
        """
        while True:
            c = file.read(chunk_size)
            if c:
                yield c
            else:
                break

    if not request.session.get('is_login', None):
        return HttpResponse('Please login in first')

    Modal = ModalInfo.objects.filter(pk=ModalID)
    if len(Modal):
        visit = Modal[0].Visit
        subjectID = visit.Subject.subjectID
        visitPhase = visit.Phase
        visitDiagnosis = visit.Diagnosis
        zipName = subjectID + '_' + visitPhase + '_' + visitDiagnosis + '_Causality'

        with tempfile.NamedTemporaryFile() as temp:
            archive = zipfile.ZipFile(temp.name, "w")
            with tempfile.TemporaryDirectory() as temp_dir:
                task = CausalityConnectivityTask.objects.get(Task_Modal_id=ModalID)
                preprocessDir = task.Preprocessed_Dir + '/Causality/Results/*'
                SSHCommand = 'scp -r ' + preprocessDir + ' ' + temp_dir + '/'
                os.system(SSHCommand)
                for file in os.listdir(temp_dir + '/'):
                    archive.write(temp_dir + '/' + file,
                                  zipName + '/' + file)
            archive.close()
            file = open(temp.name, 'rb')
            response = FileResponse(file, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=' + zipName + '.zip'
            return response

    else:
        return HttpResponseForbidden('Not found')


def ResetPreprocessingTask(request, ModalID):
    if not request.session.get('is_login', None):
        return HttpResponse('Please login in first')

    TasksToReset = CausalityConnectivityTask.objects.filter(Task_Modal_id=ModalID)
    if len(TasksToReset):
        Server = TasksToReset[0].Task_Server
        if Server:
            servers_occupied = CausalityConnectivityTask.objects.filter(Task_Server=Server).filter(Task_Start=1,
                                                                                                   Task_Finish=0)
            if len(servers_occupied) == 1:

                if servers_occupied[0] == TasksToReset[0]:
                    # print('Only One server occupied, can be reset ' + Server.Server_IP)
                    # print('Going to reset' + Server.Server_IP)
                    SSHCommand.CancelCausalityServerTask(Server)
                    isDebug = TaskQueue.objects.get(Type='CausalityConnectivity').isDebug
                    if not isDebug:
                        SSHCommand.CleanUpCausalityServer(Server)
                    # SSHCommand.RestartServer(Server)
                    Server.Server_IsBusy = False
                    Server.save()
        for task in TasksToReset:
            task.Progress_value = 0
            task.Task_Status = 200
            task.Task_Server = None
            task.Task_Finish = 0
            task.Task_Start = 0
            task.save()

    return HttpResponse('Task Reset successfully')


def CheckTasks(request, range):
    if not request.session.get('is_login', None):
        return HttpResponse('Please login in first')

    rarfileList = []
    if range == 'ALL':
        pageSize = int(request.GET.get('pageSize'))
        pageNumber = int(request.GET.get('pageNumber'))
        sortName = request.GET.get('sortName')
        sortOrder = request.GET.get('sortOrder')
        if sortOrder == 'desc':
            sortName = '-' + sortName
        uploadedFileList = []
        total = CausalityConnectivityTask.objects.all().count()
        tasks = CausalityConnectivityTask.objects.order_by(sortName)[(pageNumber - 1) * pageSize:(pageNumber) * pageSize]
        for task in tasks:
            uploadedFile = {}
            modal = task.Task_Modal
            uploadedFile['database'] = modal.DataSource
            uploadedFile['subjectID'] = modal.Visit.Subject.subjectID
            uploadedFile['group'] = modal.Visit.Diagnosis
            uploadedFile['visit'] = modal.Visit.Phase
            uploadedFile['diagnosis'] = modal.Visit.Diagnosis
            uploadedFile['Modality'] = modal.modalName
            uploadedFile['ModalID'] = modal.pk
            uploadedFile['uploader'] = modal.RARFile.uploader.name
            uploadedFile['UUID'] = modal.uuidStr

            # Manually set the time zone to China, Bocheng Wang 2021.04.21
            time = modal.RARFile.upload_time + datetime.timedelta(hours=8)
            uploadedFile['uploadedTime'] = time.strftime("%Y/%m/%d %H:%M:%S")
            if task.Task_StartTime:
                time = task.Task_StartTime + datetime.timedelta(hours=8)
                uploadedFile['startTime'] = time.strftime("%Y/%m/%d %H:%M:%S")
            if task.Task_EndTime:
                time = task.Task_EndTime + datetime.timedelta(hours=8)
                uploadedFile['endTime'] = time.strftime("%Y/%m/%d %H:%M:%S")

            Causality_task = CausalityConnectivityTask.objects.get(Task_Modal=modal)
            uploadedFile['task_start'] = Causality_task.Task_Start
            uploadedFile['task_Finish'] = Causality_task.Task_Finish
            uploadedFile['progress_value'] = Causality_task.Progress_value

            if Causality_task.Task_Server:
                uploadedFile['Server'] = Causality_task.Task_Server.Server_Name

            if Causality_task.Task_Status == -1:
                uploadedFile['Task_Status'] = -1
            else:
                uploadedFile['Task_Status'] = 200

            uploadedFileList.append(uploadedFile)
        # return HttpResponse(json.dumps(uploadedFileList))
        return HttpResponse(json.dumps({'total': total, 'rows': uploadedFileList}))
