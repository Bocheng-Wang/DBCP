# coding=utf-8
from DBCP import settings
from DBCPOnline import SSHCommand
from DBCPOnline.models import ModalInfo
from DBCP_Scheduler import ServerManagement
from DBCP_Scheduler.models import CausalityConnectivityTask, CorrelationConnectivityTask, TaskQueue
from django.utils import timezone
import logging

def onFinishedPreprocessingTask(task):
    """
    任务结束后，拷贝数据，并删除文件夹，释放服务器
    :param task:
    :return:
    """
    status = 500
    SSHCommand.onFinishTaskInSSH(task)
    task.Task_Finish = True
    task.Progress_value = 100
    task.Task_EndTime = timezone.now()
    task.save()

    ServerManagement.PopAvailableServer(task.Task_Server)
    SSHCommand.CleanUpCausalityServer(task.Task_Server)
    # SSHCommand.RestartServer(task.Task_Server)
    status = 200
    return status


def updateOwnedTaskStatus(task):
    """
    检查服务器状态
    :param task:
    :return:
    """
    status = SSHCommand.CheckCausalityThreadInServer(task.Task_Server.Server_IP)
    task.Task_Status = status
    task.save()
    return status


def AbandonTask(modal):
    """
    当预处理出现错误时，放弃该任务，释放服务器，等待用户手动删除该visit
    :param modalID: 与visit相关的所有task，包括静态和动态脑连接计算task
    :return:
    """
    logging.info('\033[1;33m ---------------------Going to Abandon this Causality task-------------------- \033[0m')
    # print('\033[0;35;46m ---------------------Going to Abandon this Causality task-------------------- \033[0m')
    tasks = CausalityConnectivityTask.objects.filter(Task_Modal=modal)

    if len(tasks):
        server = tasks[0].Task_Server
        for eachTask in tasks:
            eachTask.Task_Start = True
            eachTask.Task_Finish = True
            eachTask.Task_Status = -1
            # eachTask.Task_Server = None
            eachTask.save()

        if server:
            isDebug = TaskQueue.objects.get(Type='CausalityConnectivity').isDebug
            if not isDebug:
                SSHCommand.CleanUpCausalityServer(server)
            # SSHCommand.RestartServer(server)
            server.Server_IsBusy = False
            server.save()


def updateOwnedTaskProgressValue(task):
    """
    更新任务的预处理进度
    :param task: 格兰杰因果或新型因果关系脑连接计算任务
    :return:状态值，200，更新成功
    """
    progress_result = SSHCommand.lookupCausalityLogfileInSSH(task)
    progress_value = progress_result['value']
    progress_status = progress_result['status']
    # if progress_status == 500:
    #     AbandonTask(task.Task_Modal)
    task.Progress_value = round(float(progress_value), 2)
    task.save()
    if task.Progress_value == float('100'):
        status = onFinishedPreprocessingTask(task)
    else:
        status = updateOwnedTaskStatus(task)
        if status == -1:
            AbandonTask(task.Task_Modal)
    return


def toStartPreprocessingTask(task):
    """
    To Start Causality Analysis Task
    :param task: Causality Task in which server has been assigned
    :return: status
    """
    status = 500
    try:
        SSHCommand.toStartCausalityInSSH(task)
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
    To check and assign causality task for free server
    :return:
    """
    if taskPrefer:
        preprocess_task_list = [taskPrefer]
    else:
        preprocess_task_list = CausalityConnectivityTask.objects.filter(Task_Start=False)
    if len(preprocess_task_list):
        for task in preprocess_task_list:
            server = ServerManagement.AquireAvailableServer('Causality')
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
    preprocess_task_list = CausalityConnectivityTask.objects.filter(Task_Start=1, Task_Finish=0)
    print(
        '=======================Found ' + str(len(preprocess_task_list)) + ' Tasks to causality analyasis=============')
    for task in preprocess_task_list:
        if task.Task_Start and not task.Task_Finish:
            # print('------- Found Running Preprocessing Task  -- ID: ' + str(
            #     task.id) + '  -- Owner: ' + task.Task_Modal.RARFile.uploader.name)

            updateOwnedTaskProgressValue(task)
            # status = updateOwnedTaskStatus(task)
            # if status == -1:
            #     AbandonTask(task.Task_Modal)
    check_and_submitTask(taskPrefer=None)
    return
