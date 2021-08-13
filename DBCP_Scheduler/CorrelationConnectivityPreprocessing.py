# coding=utf-8
from DBCPOnline import SSHCommand
from django.utils import timezone

from DBCP_Scheduler import ServerManagement

from DBCP_Scheduler.models import CausalityConnectivityTask, TaskQueue
import threading

from apscheduler.schedulers.background import BackgroundScheduler
from django.shortcuts import render
from django.utils import timezone
# Create your views here.
from DBCPOnline import SSHCommand
from DBCP_Scheduler.models import CorrelationConnectivityTask


def onFinishedPreprocessingTask(task):
    status = 500
    SSHCommand.onFinishParcellationAndCorrelationinSSH(task)
    task.Task_Finish = True
    task.Progress_value = 100
    task.Task_EndTime = timezone.now()
    task.save()
    ServerManagement.PopAvailableServer(task.Task_Server)
    if task.Preprocess_Type == 'Static':
        preprocessTaskList = CorrelationConnectivityTask.objects.filter(Task_Modal=task.Task_Modal,
                                                                        Preprocess_Type='Dynamic')
        taskDynamic = preprocessTaskList[0]
        taskDynamic.Task_Server = task.Task_Server
        taskDynamic.save()
        check_and_submitTask(taskPrefer=taskDynamic)

        # create Causality Task
    elif task.Preprocess_Type == 'Dynamic':
        taskTMP = CausalityConnectivityTask.objects.filter(Task_Modal=task.Task_Modal)
        if not len(taskTMP):
            causalityTask = CausalityConnectivityTask.objects.create(Task_Modal=task.Task_Modal, Task_Status=200,
                                                                 Task_Type='Causality',
                                                                 Preprocessed_Dir=task.Preprocessed_Dir)
            causalityTask.save()
        isDebug = TaskQueue.objects.get(Type='CorrelationConnectivity').isDebug
        if not isDebug:
            SSHCommand.CleanUpParcellationServer(task.Task_Server)
        SSHCommand.RestartServer(task.Task_Server)

    status = 200
    return status


def updateOwnedTaskStatus(task):
    """
    检查服务器状态
    :param task:
    :return:
    """
    status = SSHCommand.CheckParcellationThreadInServer(task.Task_Server.Server_IP)
    task.Task_Status = status
    task.save()
    return status


def updateOwnedTaskProgressValue(task):
    """
    更新任务的预处理进度
    :param task: 静态或动态脑链接计算任务
    :return:状态值，200，更新成功,300 查询异常
    """
    progress_result = SSHCommand.lookupParcellationAndCorrelationLogFilesInSSH(task)
    progress_value = progress_result['value']
    progress_status = progress_result['status']
    # if progress_status == 500:
    #     AbandonTask(task.Task_Modal)
    task.Progress_value = round(float(progress_value), 2)
    task.save()
    if progress_value == '100':
        status = onFinishedPreprocessingTask(task)
    else:
        status = updateOwnedTaskStatus(task)
        if status == -1:
            AbandonTask(task.Task_Modal)
    return


def toStartPreprocessingTask(task):
    status = 500
    try:
        SSHCommand.toStartParcellationAndCorrelationInSSH(task)
        task.Task_StartTime = timezone.now()
        task.Task_Start = True
        task.Task_Status = 200
        task.Preprocessed_Dir = '/'.join(
            task.Task_Modal.RARFile.storage_path.split('/')[0:4]) + '/Preprocessed/' + task.Task_Modal.uuidStr
        server = task.Task_Server
        server.Server_IsBusy = True
        server.save()
        task.save()
        status = 200
    except:
        status = 500
    # print(
    #     'task start with error. Task ID:' + str(task.id) + '   -- Owner: ' + task.Task_Modal.RARFile.uploader.name)
    return status


def check_and_submitTask(taskPrefer):
    """
    检查是否存在空闲服务器，分配任务处理。如果是 动态脑链接 计算任务，不分配新的服务器，只在原服务器上计算
    """

    if taskPrefer:
        preprocess_task_list = [taskPrefer]
    else:
        preprocess_task_list = CorrelationConnectivityTask.objects.filter(Task_Start=False)
    if len(preprocess_task_list):
        for task in preprocess_task_list:
            if task.Task_Server and (task.Preprocess_Type == 'Dynamic'):
                busy = ServerManagement.CheckServerIsBusy(task.Task_Server)
                if busy is False:
                    resultCode = toStartPreprocessingTask(task)
                    if resultCode == 200:
                        break
                    elif resultCode == 500:
                        continue
            elif task.Preprocess_Type == 'Static':
                server = ServerManagement.AquireAvailableServer('Parcellation')
                if server:
                    busy = ServerManagement.CheckServerIsBusy(server)
                    if busy is False:
                        task.Task_Server = server
                        resultCode = toStartPreprocessingTask(task)
                        if resultCode == 200:
                            break
                        elif resultCode == 500:
                            continue
    return


def checkTaskStatus():
    """
    检查是否存在 静态或动态脑连接 相关性矩阵的计算任务。
    判断标志：Task_Start = 1 && Task_Finish = 0
    :return:
    """
    preprocess_task_list = CorrelationConnectivityTask.objects.filter(Task_Start=1, Task_Finish=0)
    print('=======================Found ' + str(len(preprocess_task_list)) + ' Tasks to parcellate=============')
    for task in preprocess_task_list:
        if task.Task_Start and not task.Task_Finish:
            # print('------- Found Running Preprocessing Task  -- ID: ' + str(
            #     task.id) + '  -- Owner: ' + task.Task_Modal.RARFile.uploader.name)

            updateOwnedTaskProgressValue(task)
            # status = updateOwnedTaskStatus(task)
            # if status == -1:
            #     AbandonTask(task.Task_Modal)
    check_and_submitTask(taskPrefer=None)


def AbandonTask(modal):
    """
    当预处理出现错误时，放弃该任务，释放服务器，等待用户手动删除该visit
    :param modalID: 与visit相关的所有task，包括静态和动态脑连接计算task
    :return:
    """
    print('\033[0;35;46m ---------------------Going to Abandon this Parcellation task-------------------- \033[0m')
    tasks = CorrelationConnectivityTask.objects.filter(Task_Modal=modal)

    if len(tasks):
        server = tasks[0].Task_Server
        for eachTask in tasks:
            eachTask.Task_Start = True
            eachTask.Task_Finish = True
            eachTask.Task_Status = -1
            # eachTask.Task_Server = None
            eachTask.save()
        if server:
            server.Server_IsBusy = False
            server.save()
