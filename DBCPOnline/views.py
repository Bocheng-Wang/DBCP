# coding=utf-8
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
from DBCP_Scheduler.models import CorrelationConnectivityTask, CausalityConnectivityTask, Server, TaskQueue
from UserManagement.models import User

from django.http import FileResponse
import scipy.io as scio

import seaborn as sns
from matplotlib import pyplot


def Usage(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'DBCPOnline/Usage.html', {"currentIP": currentIP,
                                                     'total_visit': totalVisit})


def Preparation(request):
    if not request.session.get('is_login', None):
        return render(request, 'DBCPOnline/Preparation.html')
    authorized = checkAuthorization(userid=request.session['user_id'])
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'DBCPOnline/Preparation.html', {"currentIP": currentIP,
                                                           'authorized': authorized,
                                                           'total_visit': totalVisit})


def getDetailRecords():
    tasks = CorrelationConnectivityTask.objects.filter(Task_Finish=1, Task_Status=200)
    completeRecords = len(tasks)

    tasks = CorrelationConnectivityTask.objects.filter(Task_Finish=1, Task_Status=-1)
    FailedRecords = round(len(tasks) / 2)

    tasks = CorrelationConnectivityTask.objects.all()
    totalRecords = len(tasks)

    tasks = CorrelationConnectivityTask.objects.filter(Task_Start=1, Task_Finish=0)
    runningRecords = len(tasks)

    waitingRecords = len(CorrelationConnectivityTask.objects.filter(Task_Start=0))

    totalServer = len(Server.objects.filter(Server_Type='Parcellation'))
    idleServer = len(Server.objects.filter(Server_Type='Parcellation', Server_IsBusy=False))

    LiLei = round(len(CorrelationConnectivityTask.objects.filter(Task_Modal__RARFile__uploader_id=48)) / 2)
    PengLong = round(len(CorrelationConnectivityTask.objects.filter(Task_Modal__RARFile__uploader_id=53)) / 2)
    WangYipei = round(len(CorrelationConnectivityTask.objects.filter(Task_Modal__RARFile__uploader_id=54)) / 2)
    Test = round(len(CorrelationConnectivityTask.objects.filter(Task_Modal__RARFile__uploader_id=50)) / 2)
    Daikexuan = round(len(CorrelationConnectivityTask.objects.filter(Task_Modal__RARFile__uploader_id=57)) / 2)
    Jiangzhuolin = round(len(CorrelationConnectivityTask.objects.filter(Task_Modal__RARFile__uploader_id=55)) / 2)

    return totalRecords, completeRecords, runningRecords, FailedRecords, totalServer, idleServer, LiLei, PengLong, WangYipei, Test, waitingRecords, Daikexuan, Jiangzhuolin


# here we assume the number of dynamic windows is fixed 125
def checkAuthorization(userid):
    user = User.objects.get(id=userid)
    if user.name == '王博丞':
        return True
    else:
        return False


def Preprocessing(request):
    if not request.session.get('is_login', None):
        return render(request, 'DBCPOnline/Preprocessing.html')
    context = {
        'dynamicWindowNumber': range(1, 126),
    }
    currentIP, totalVisit = VisitStatistic.change_info(request)
    totalRecords, completeRecords, runningRecords, FailedRecords, totalServer, idleServer, LiLei, PengLong, WangYipei, Test, waitingRecords, Daikexuan, Jiangzhuolin = getDetailRecords()
    schedulerStatus = getschedulerStatus(type='CorrelationConnectivity')
    authorized = checkAuthorization(userid=request.session['user_id'])
    return render(request, 'DBCPOnline/Preprocessing.html', {'context': context,
                                                             "currentIP": currentIP,
                                                             'total_visit': totalVisit,
                                                             'totalRecords': totalRecords,
                                                             'runningRecords': runningRecords,
                                                             'completeRecords': completeRecords,
                                                             'runningServer': totalServer - idleServer,
                                                             'waitingRecords': waitingRecords,
                                                             'idleServer': idleServer,
                                                             'deadServer': totalServer - idleServer - runningRecords,
                                                             'LiLei': LiLei,
                                                             'Aaron08131': PengLong,
                                                             'WangYipei': WangYipei,
                                                             'Daikexuan': Daikexuan,
                                                             'Jiangzhuolin': Jiangzhuolin,
                                                             'schedulerStatus': schedulerStatus,
                                                             'Test': Test,
                                                             'authorized': authorized,
                                                             'FailedRecords': FailedRecords})


def Visualization(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'DBCPOnline/Visualization.html', {"currentIP": currentIP,
                                                             'total_visit': totalVisit})


def TopologicalAnalysis(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'DBCPOnline/TopologicalAnalysis.html', {"currentIP": currentIP,
                                                                   'total_visit': totalVisit})


def DeepLearning(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'DBCPOnline/DeepLearning.html', {"currentIP": currentIP,
                                                            'total_visit': totalVisit})


def getDetailKBCARecords():
    tasks = CausalityConnectivityTask.objects.filter(Task_Finish=1, Task_Status=200)
    completeRecords = len(tasks)

    tasks = CausalityConnectivityTask.objects.filter(Task_Finish=1, Task_Status=-1)
    FailedRecords = len(tasks)

    tasks = CausalityConnectivityTask.objects.all()
    totalRecords = len(tasks)

    tasks = CausalityConnectivityTask.objects.filter(Task_Start=1, Task_Finish=0)
    runningRecords = len(tasks)

    waitingRecords = len(CausalityConnectivityTask.objects.filter(Task_Start=0))

    totalServer = len(Server.objects.filter(Server_Type='Causality'))
    idleServer = len(Server.objects.filter(Server_Type='Causality', Server_IsBusy=False))

    return totalRecords, completeRecords, runningRecords, FailedRecords, totalServer, idleServer, waitingRecords


def getschedulerStatus(type):
    status = TaskQueue.objects.get(Type=type).isScheduled
    if status == 1:
        return 'checked'
    else:
        return ''


def KBCAAnalysis(request):
    if not request.session.get('is_login', None):
        return render(request, 'DBCPOnline/KBCAAnalysis.html')
    authorized = checkAuthorization(userid=request.session['user_id'])
    currentIP, totalVisit = VisitStatistic.change_info(request)
    totalRecords, completeRecords, runningRecords, FailedRecords, totalServer, idleServer, waitingRecords = getDetailKBCARecords()
    schedulerStatus = getschedulerStatus(type='CausalityConnectivity')
    return render(request, 'DBCPOnline/KBCAAnalysis.html', {
        "currentIP": currentIP,
        'total_visit': totalVisit,
        'authorized': authorized,
        'totalRecords': totalRecords,
        'runningRecords': runningRecords,
        'completeRecords': completeRecords,
        'runningServer': totalServer - idleServer,
        'waitingRecords': waitingRecords,
        'idleServer': idleServer,
        'deadServer': totalServer - idleServer - runningRecords,
        'schedulerStatus': schedulerStatus,
        'FailedRecords': FailedRecords})


def JHCPMMP(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'DBCPOnline/JHCPMMP.html', {"currentIP": currentIP,
                                                       'total_visit': totalVisit})


def Hypothesis(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'DBCPOnline/Hypothesis.html', {"currentIP": currentIP,
                                                          'total_visit': totalVisit})


def Multimodal(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'DBCPOnline/Multimodal.html', {"currentIP": currentIP,
                                                          'total_visit': totalVisit})


def DBCP(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'DBCPOnline/DBCPOnline.html', {"currentIP": currentIP,
                                                          'total_visit': totalVisit})


def FileUpload(request):
    if request.method == "POST":
        if not request.session.get('is_login', None):
            return HttpResponse("Please Login in first")
        if len(request.FILES) == 1:
            # filename should like ADNI2_002_S_0295.zip
            filename = request.FILES["file"].name
            group = request.POST['group']
            age = float(request.POST['age'])
            phase = request.POST['visit']
            filename = filename[0:-4] + '_' + phase + filename[-4:]
            if group not in ['0.HC', '2.EMCI', '4.LMCI', '5.AD']:
                return HttpResponse("分组错误")
            if phase not in ['BL', 'SC', 'M03', 'M06', 'M12', 'M24', 'M36', 'M48', 'M60']:
                return HttpResponse('Visit Info Error')
            if age > 150 or age <= 0:
                return HttpResponse('Age Info Error')
            with open(filename, 'wb') as f:
                for chunk in request.FILES['file'].chunks():
                    f.write(chunk)

            # to check zip file 2021.05.26
            try:
                if (zipfile.ZipFile(file=filename, mode="r").testzip()):
                    DeleteCMD = 'rm -rf ' + filename
                    os.system(DeleteCMD)
                    return HttpResponse('500')
            except:
                return HttpResponse('500')

            DBCPStorageIP = settings.CUSTOM_SETTINGS['DBCP.Storage.Server']
            storagePath = ':/root/DBCP.Data/' + group + '/Original/'

            user = User.objects.get(id=request.session['user_id'])
            filesize = os.path.getsize(os.path.join(settings.BASE_DIR, filename))
            storage_path = DBCPStorageIP + storagePath + filename
            rarFile = RARFile.create(user, timezone.now(), filename, filesize, storage_path)
            subjectID = filename[6:16]
            subject = Subject.objects.filter(subjectID=subjectID).first()
            if subject is None:
                subject = Subject.create(subjectID)
                subject.save()
            visit = Visit.objects.filter(Subject=subject, Phase=phase)
            if len(visit):
                return HttpResponse("已存在相应随访记录")
            visit = Visit.create(subject, age, phase, group[2:])
            modal = ModalInfo.create('MRI', filename[0:5], visit, rarFile, str(uuid.uuid4()))
            # Copy file to DBCPStorage
            SSHCommand = 'scp ' + filename + ' ' + 'root@' + DBCPStorageIP + storagePath
            os.system(SSHCommand)
            DeleteCMD = 'rm -rf ' + filename
            os.system(DeleteCMD)

            rarFile.save()
            visit.save()
            modal.save()
            static_task = CorrelationConnectivityTask.objects.create(Preprocess_Type='Static', Task_Modal=modal)
            dynamic_task = CorrelationConnectivityTask.objects.create(Preprocess_Type='Dynamic', Task_Modal=modal)

            static_task.save()
            dynamic_task.save()

            return HttpResponse('200')
        else:
            return HttpResponse('-1')


def Find_Visit_By_SubjectID(request):
    if not request.session.get('is_login', None):
        return HttpResponse('Please login in first')
    subjectID = request.POST['subjectID']
    Visits = [modal.Visit for modal in ModalInfo.objects.filter(RARFile__uploader=request.session['user_id'],
                                                                Visit__in=Visit.objects.filter(
                                                                    Subject__subjectID=subjectID))]
    visitList = []
    for visit in Visits:
        visitRecord = {}
        visitRecord['Visit_age'] = visit.Visit_age
        visitRecord['Visit_ID'] = visit.pk
        visitRecord['Phase'] = visit.Phase
        visitRecord['Diagnosis'] = visit.Diagnosis
        visitRecord['visit_time'] = visit.visit_time.strftime("%Y/%m/%d %H:%M:%S")
        visitRecord['ModalID'] = ModalInfo.objects.get(Visit=visit).pk
        visitRecord['MMSE'] = visit.MMSE
        visitRecord['CDR'] = visit.CDR
        visitRecord['SubjectID'] = subjectID
        visitRecord['uploader'] = request.session['user_id']

        IsCIFTIFY_Finished = False
        taskStart = CorrelationConnectivityTask.objects.filter(Task_Modal__Visit_id=visit.pk)[0].Task_Start
        taskEnd = CorrelationConnectivityTask.objects.filter(Task_Modal__Visit_id=visit.pk)[0].Task_Finish
        if taskStart:
            if taskEnd:
                IsCIFTIFY_Finished = True
        visitRecord['IsCIFTIFY_Finished'] = IsCIFTIFY_Finished

        visitList.append(visitRecord)
    return HttpResponse(json.dumps(visitList))


def toDeletePreprocessFolders(modal):
    status = 500
    # try:
    taskList = CausalityConnectivityTask.objects.filter(Task_Modal=modal)
    for task in taskList:
        SSHCommand.toDeleteCausalityProgressFolderInSSH(task)

    taskList = CorrelationConnectivityTask.objects.filter(Task_Modal=modal)
    for task in taskList:
        SSHCommand.toDeleteParcellationAndCorrelationPreprocessFolderInSSH(task)
    status = 200
    # except:
    #     status = 500
    #     print(
    #         'task folder delete with error. Task ID:' + str(task.id) + '   -- Owner: ' + task.Task_Modal.RARFile.uploader.name)
    return status


def getNIIfile(request, visitID):
    if not request.session.get('is_login', None):
        return HttpResponse('Please login in first')

    Visit_ID = visitID
    if Visit_ID != 'example':
        Task = CorrelationConnectivityTask.objects.filter(Task_Modal__Visit_id=Visit_ID)[0]
        MRIDir = Task.Preprocessed_Dir + '/*/fmriprep/input/*/anat/*.nii'
        fMRIFile = Task.Preprocessed_Dir + '/*/fmriprep/input/*/func/*.nii'

        with tempfile.TemporaryDirectory() as fileDir:
            fileDir += os.sep
            SSHCommand = 'scp -r ' + MRIDir + ' ' + fileDir
            os.system(SSHCommand)

            list_file = os.listdir(fileDir)[0]
            file = open(fileDir + list_file, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;'
            return response
    elif Visit_ID == 'example':
        list_file = './static/DBCPExamples/sub-ADNI2002S0295_T1w.nii'
        file = open(list_file, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;'
        return response


def checkUploadedFiles(request, range):
    if not request.session.get('is_login', None):
        return HttpResponse('Please login in first')

    rarfileList = []
    if range == 'MY':
        user = User.objects.get(id=request.session['user_id'])
        rarfileList = RARFile.objects.filter(uploader=user)
    elif range == 'ALL':
        pageSize = int(request.GET.get('pageSize'))
        pageNumber = int(request.GET.get('pageNumber'))
        sortName = request.GET.get('sortName')
        sortOrder = request.GET.get('sortOrder')
        if sortOrder == 'desc':
            sortName = '-' + sortName
        total = RARFile.objects.all().count()
        rarfileList = RARFile.objects.order_by(sortName)[(pageNumber - 1) * pageSize:(pageNumber) * pageSize]
        # Check preprocessing task in period
        # global job_is_start
        # if job_is_start is False:
        #     sched = BackgroundScheduler()
        #     sched.add_job(checkTaskStatus, trigger='interval', max_instances=1, args=(request.session['user_id'],),
        #                   seconds=10)
        #     sched.start()
        #     job_threading_lock.acquire()
        #     job_is_start = True
        #     job_threading_lock.release()
    uploadedFileList = []
    for eachfile in rarfileList:
        uploadedFile = {}
        modal = ModalInfo.objects.get(RARFile=eachfile)
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

        static_task = CorrelationConnectivityTask.objects.get(Task_Modal=modal, Preprocess_Type='Static')
        uploadedFile['static_task_start'] = static_task.Task_Start
        uploadedFile['static_task_Finish'] = static_task.Task_Finish
        uploadedFile['static_progress_value'] = static_task.Progress_value

        if static_task.Task_Server:
            uploadedFile['Server'] = static_task.Task_Server.Server_Name

        dynamic_task = CorrelationConnectivityTask.objects.get(Task_Modal=modal, Preprocess_Type='Dynamic')
        uploadedFile['dynamic_task_start'] = dynamic_task.Task_Start
        uploadedFile['dynamic_task_Finish'] = dynamic_task.Task_Finish
        uploadedFile['dynamic_progress_value'] = dynamic_task.Progress_value
        if (dynamic_task.Task_EndTime):
            time = dynamic_task.Task_EndTime + datetime.timedelta(hours=8)
            uploadedFile['dynamic_end_time'] = time.strftime("%Y/%m/%d %H:%M:%S")

        if dynamic_task.Task_Status == -1 or static_task.Task_Status == -1:
            uploadedFile['Task_Status'] = -1
        else:
            uploadedFile['Task_Status'] = 200

        uploadedFileList.append(uploadedFile)
    # return HttpResponse(json.dumps(uploadedFileList))
    if range == 'MY':
        return HttpResponse(json.dumps(uploadedFileList))
    elif range == 'ALL':
        return HttpResponse(json.dumps({'total': total, 'rows': uploadedFileList}))


def checkUploadedSubjects(request, range):
    if not request.session.get('is_login', None):
        return HttpResponse('Please login in first')

    rarfileList = []
    if range == 'MY':
        user = User.objects.get(id=request.session['user_id'])
        rarfileList = RARFile.objects.filter(uploader=user)
        subjects = [modal.Visit.Subject for modal in ModalInfo.objects.filter(RARFile__in=rarfileList)]
        subjects = list(set(subjects))
    elif range == 'ALL':
        rarfileList = RARFile.objects.all()
        subjects = [modal.Visit.Subject for modal in ModalInfo.objects.filter(RARFile__in=rarfileList)]
        subjects = list(set(subjects))
        # Check preprocessing task in period
        # global job_is_start
        # if job_is_start is False:
        #     sched = BackgroundScheduler()
        #     sched.add_job(checkTaskStatus, trigger='interval', max_instances=1, args=(request.session['user_id'],),
        #                   seconds=10)
        #     sched.start()
        #     job_is_start = True
    uploadedSubjectList = []
    for subject in subjects:
        subjectRecord = {}
        subjectRecord['subjectID'] = subject.subjectID
        subjectRecord['sex'] = subject.sex
        subjectRecord['education_years'] = subject.education_years
        subjectRecord['career'] = subject.career
        subjectRecord['uploader'] = request.session['user_id']
        uploadedSubjectList.append(subjectRecord)
    return HttpResponse(json.dumps(uploadedSubjectList))


def cancelPreprocess(request):
    if not request.session.get('is_login', None):
        return HttpResponse('无权限')
    user = User.objects.get(id=request.session['user_id'])
    modalID = request.POST['ModalID']
    modal = ModalInfo.objects.get(pk=modalID)
    if modal.RARFile.uploader != user:
        return HttpResponse('无权限')
    try:
        toDeletePreprocessFolders(modal)
        return HttpResponse('Success in Preprocessing cancel')
    except:
        return HttpResponse('Error in Preprocessing cancel')


# delete visit uploaded by userID
def DeleteVisitTmp(request, userID):
    user = User.objects.get(id=userID)

    modals = ModalInfo.objects.filter(RARFile__uploader=user)
    for modal in modals:
        modalID = modal.pk
        # try:
        # 顺序不能换，按序删除RAR文件、Visit记录和Modal记录（外键，联动删除）
        toDeletePreprocessFolders(modal)
        ModalInfo.objects.get(pk=modalID).RARFile.delete()
        ModalInfo.objects.get(pk=modalID).Visit.delete()
    return HttpResponse('Success in visit delete')
    # except:
    #     return HttpResponse('Error in visit delete')

    # except:
    #     return HttpResponse('Error occurs in visit delete')


# delete visit  by modalID
def DeleteVisitByModalIDTmp(request, pwd, modalID):
    if pwd != '7788':
        return HttpResponse('Not allowed!')
    modals = ModalInfo.objects.filter(pk=modalID)
    for modal in modals:
        # try:
        # 顺序不能换，按序删除RAR文件、Visit记录和Modal记录（外键，联动删除）
        toDeletePreprocessFolders(modal)
        ModalInfo.objects.get(pk=modalID).RARFile.delete()
        ModalInfo.objects.get(pk=modalID).Visit.delete()
    return HttpResponse('Success in visit delete')
    # except:
    #     return HttpResponse('Error in visit delete')

    # except:
    #     return HttpResponse('Error occurs in visit delete')


def getDebugInfo(type):
    status = TaskQueue.objects.get(Type=type).isDebug
    if status == 1:
        return 'checked'
    else:
        return ''


def getTaskLastRunInfo(type):
    t = TaskQueue.objects.get(Type=type).Task_LastRunTime + datetime.timedelta(hours=8)
    return t.strftime("%Y/%m/%d %H:%M:%S")


def Manage(request):
    if not request.session.get('is_login', None):
        return render(request, 'DBCPOnline/Manage.html')
    user = User.objects.get(id=request.session['user_id'])
    if user.name != '王博丞':
        return HttpResponse('无权限')
    currentIP, totalVisit = VisitStatistic.change_info(request)
    parcellation_schedulerStatus = getschedulerStatus(type='CorrelationConnectivity')
    causality_schedulerStatus = getschedulerStatus(type='CausalityConnectivity')
    parcellation_debug = getDebugInfo(type='CorrelationConnectivity')
    causality_debug = getDebugInfo(type='CausalityConnectivity')
    causalityLastRunTime = getTaskLastRunInfo(type='CausalityConnectivity')
    parcellationLastRunTime = getTaskLastRunInfo(type='CorrelationConnectivity')
    authorized = checkAuthorization(userid=request.session['user_id'])
    return render(request, 'DBCPOnline/Manage.html', {"currentIP": currentIP,
                                                      'parcellation_schedulerStatus': parcellation_schedulerStatus,
                                                      'causality_schedulerStatus': causality_schedulerStatus,
                                                      'parcellation_debug': parcellation_debug,
                                                      'causality_debug': causality_debug,
                                                      'parcellationLastRunTime': parcellationLastRunTime,
                                                      'causalityLastRunTime': causalityLastRunTime,
                                                      'authorized': authorized,
                                                      'total_visit': totalVisit})


def MigrateModal(request, ModalID, toServerIP):
    if not request.session.get('is_login', None):
        return HttpResponse("Please Login in first")
    authorized = checkAuthorization(userid=request.session['user_id'])
    if not authorized:
        return HttpResponse("Not authorized")

    modalID = ModalID
    toServerIP = toServerIP

    status = SSHCommand.MigrateModal(ModalID, toServerIP)
    if status == 500:
        return HttpResponse('Failed')
    return HttpResponse('Migration Successed')


def CheckAvaliabletoMigrate(request):
    if not request.session.get('is_login', None):
        return HttpResponse("Please Login in first")
    authorized = checkAuthorization(userid=request.session['user_id'])
    if not authorized:
        return HttpResponse("Not authorized")

    rarfileList = []
    uploadedFileList = []
    tasks = CausalityConnectivityTask.objects.all()
    for task in tasks:
        if task.Task_Start and not task.Task_Finish:
            continue
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
        uploadedFile['fromServer'] = task.Preprocessed_Dir.split(':')[0]
        uploadedFile['toServer'] = []
        for server in Server.objects.filter(Server_Type='Storage'):
            uploadedFile['toServer'].append(server.Server_IP)

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
    return HttpResponse(json.dumps(uploadedFileList))


def Migration(request):
    if not request.session.get('is_login', None):
        return HttpResponse("Please Login in first")
    authorized = checkAuthorization(userid=request.session['user_id'])
    currentIP, totalVisit = VisitStatistic.change_info(request)
    totalRecords, completeRecords, runningRecords, FailedRecords, totalServer, idleServer, waitingRecords = getDetailKBCARecords()
    schedulerStatus = getschedulerStatus(type='CausalityConnectivity')
    return render(request, 'DBCPOnline/Migration.html', {
        "currentIP": currentIP,
        'total_visit': totalVisit,
        'authorized': authorized,
        'totalRecords': totalRecords,
        'runningRecords': runningRecords,
        'completeRecords': completeRecords,
        'runningServer': totalServer - idleServer,
        'waitingRecords': waitingRecords,
        'idleServer': idleServer,
        'deadServer': totalServer - idleServer - runningRecords,
        'schedulerStatus': schedulerStatus,
        'FailedRecords': FailedRecords})


def CleanUPServer(request):
    servers = Server.objects.all()
    for server in servers:
        IP = server.Server_IP
        print(IP)
        command = 'ssh root@' + IP + ' mv /root/projects/DataForPreprocess/Data/fmriprep_for_analysis/ /root/projects/DataForPreprocess/'
        os.system(command)

        command = 'ssh root@' + IP + ' rm -rf /root/projects/DataForPreprocess/Data/*'
        os.system(command)

        command = 'ssh root@' + IP + ' mv /root/projects/DataForPreprocess/fmriprep_for_analysis /root/projects/DataForPreprocess/Data'
        os.system(command)
    return HttpResponse('Success')


def DeleteVisit(request):
    if not request.session.get('is_login', None):
        return HttpResponse('无权限')
    user = User.objects.get(id=request.session['user_id'])
    modalID = request.POST['ModalID']
    modal = ModalInfo.objects.get(pk=modalID)
    if modal.RARFile.uploader != user:
        return HttpResponse('无权限')
    # try:
    # 顺序不能换，按序删除RAR文件、Visit记录和Modal记录（外键，联动删除）
    toDeletePreprocessFolders(modal)
    CorrelationConnectivityTask.objects.filter(Task_Modal_id=modalID).delete()
    ModalInfo.objects.get(pk=modalID).RARFile.delete()
    ModalInfo.objects.get(pk=modalID).Visit.delete()
    return HttpResponse('Success in visit delete')
    # except:
    #     return HttpResponse('Error in visit delete')

    # except:
    #     return HttpResponse('Error occurs in visit delete')


def getHeatMap(request, ModalID, type, windowIndex):
    if not request.session.get('is_login', None):
        return HttpResponse('Please login in first')

    # type = Static or Dynamic
    # windowIndex range from 1:125
    ModalID = ModalID
    type = type
    windowIndex = windowIndex
    key_in_Matrix = 'connectivity'
    if type == 'Dynamic':
        windowIndex = windowIndex + '.mat'
    elif type == 'Static':
        windowIndex = 'staticConnectivity.mat'

    if ModalID != 'example':
        tasks = CorrelationConnectivityTask.objects.filter(Task_Modal_id=ModalID)
        if len(tasks):
            Connectivity_Dir = tasks[0].Preprocessed_Dir + '/*/Connectivity/' + type + 'Connectivity/'
            try:
                tmpFolder = '/tmp/' + str(uuid.uuid4()) + '/'
                SSHCommand = 'mkdir ' + tmpFolder
                os.system(SSHCommand)

                local_file = tmpFolder + windowIndex
                remote_file = Connectivity_Dir + windowIndex
                SSHCommand = 'scp ' + remote_file + ' ' + local_file
                os.system(SSHCommand)
                MatrixData = scio.loadmat(local_file)
                sns.set_theme()
                ax = sns.heatmap(MatrixData[key_in_Matrix], cmap='rainbow', xticklabels=False, yticklabels=False,
                                 cbar=False)
                s1 = ax.get_figure()
                filename = tmpFolder + str(uuid.uuid4()) + '.jpg'
                s1.savefig(filename, dpi=50, bbox_inches='tight')

                with open(filename, 'rb') as image:
                    file = image.read()
                imageBase64 = base64.b64encode(file)
                return HttpResponse(imageBase64, content_type='image/jpeg')
            except:
                return HttpResponse('Visit folder not found')
        else:
            return HttpResponse('Visit does not exist !')
    elif ModalID == 'example':
        Connectivity_Dir = './static/DBCPExamples/Connectivity/' + type + 'Connectivity/'
        local_file = Connectivity_Dir + os.listdir(Connectivity_Dir)[windowIndex]
        MatrixData = scio.loadmat(local_file)
        sns.set_theme()
        ax = sns.heatmap(MatrixData[key_in_Matrix], cmap='rainbow', xticklabels=False, yticklabels=False, cbar=False)
        s1 = ax.get_figure()
        filename = '/tmp/' + str(uuid.uuid4()) + '.jpg'
        s1.savefig(filename, dpi=50, bbox_inches='tight')

        file = open(filename, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'image/jpg'
        response['Content-Disposition'] = 'inline;'
        return response


def getConnectivityFiles(request, ModalID):
    def file_iterator(file, chunk_size=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
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
        zipName = subjectID + '_' + visitPhase + '_' + visitDiagnosis + '_Correlation'

        with tempfile.NamedTemporaryFile() as temp:
            archive = zipfile.ZipFile(temp.name, "w")
            with tempfile.TemporaryDirectory() as temp_dir:
                tasks = CorrelationConnectivityTask.objects.filter(Task_Modal_id=ModalID)
                for task in tasks:
                    preprocessDir = task.Preprocessed_Dir + '/*/Connectivity/' + task.Preprocess_Type + 'Connectivity/'
                    SSHCommand = 'scp -r ' + preprocessDir + ' ' + temp_dir + '/'
                    os.system(SSHCommand)
                    for file in os.listdir(temp_dir + '/' + task.Preprocess_Type + 'Connectivity/'):
                        archive.write(temp_dir + '/' + task.Preprocess_Type + 'Connectivity/' + file,
                                      zipName + '/' + task.Preprocess_Type + 'Connectivity/' + file)
            archive.close()
            file = open(temp.name, 'rb')
            response = FileResponse(file, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=' + zipName + '.zip'
            return response

    else:
        return HttpResponse('Not found')


def ResetPreprocessingTask(request, ModalID):
    if not request.session.get('is_login', None):
        return HttpResponse('Please login in first')

    TasksToReset = CorrelationConnectivityTask.objects.filter(Task_Modal_id=ModalID)
    if len(TasksToReset):
        Server = TasksToReset[0].Task_Server
        if Server:
            servers_occupied = CorrelationConnectivityTask.objects.filter(Task_Server=Server).filter(Task_Start=1,
                                                                                                     Task_Finish=0)
            if len(servers_occupied) == 1:

                if servers_occupied[0] == TasksToReset[0]:
                    # print('Only One server occupied, can be reset ' + Server.Server_IP)
                    # print('Going to reset' + Server.Server_IP)
                    isDebug = TaskQueue.objects.get(Type='CorrelationConnectivity').isDebug
                    if not isDebug:
                        SSHCommand.CleanUpParcellationServer(Server)  # 可能清除掉动态脑连接预处理文件目录，谨慎使用
                    SSHCommand.RestartServer(Server)
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


def CheckParcellationPreprocessingTask(request, ModalID):
    """
    检查服务器上的脑分区进程是否正常
    :param request:
    :param ModalID:
    :return:
    """
    if not request.session.get('is_login', None):
        return HttpResponse('Please login in first')
    result = 'Task not assigned'
    TasksToReset = CorrelationConnectivityTask.objects.filter(Task_Modal_id=ModalID)
    if len(TasksToReset):
        if (TasksToReset[0].Task_Server):
            Server_IP = TasksToReset[0].Task_Server.Server_IP
            result = SSHCommand.CheckParcellationThreadInServer(Server_IP)
    return HttpResponse(result)
