# coding=utf-8
import logging
import threading
import time
import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponseForbidden, HttpResponse

from DBCP_Scheduler import CorrelationConnectivityPreprocessing, CausalityConnectivityPreprocessing, ServerManagement
from DBCP_Scheduler.models import TaskQueue
from django.utils import timezone

threads = []


def ServerSchedulerSwitch(request, type, switch):
    if not request.session.get('is_login', None):
        return HttpResponse('Please login in first')
    queue = TaskQueue.objects.get(Type=type)
    message = ''
    if queue:
        if switch == 'off':
            queue.isScheduled = False
            queue.save()
            message = 'Task Scheduler is suspended'
        else:
            queue.isScheduled = True
            queue.save()
            message = 'Task Scheduler is running'
        return HttpResponse(message)
    else:
        return HttpResponse('Task Scheduler does not exist')


def DebugSwitch(request, type, switch):
    if not request.session.get('is_login', None):
        return HttpResponse('Please login in first')
    queue = TaskQueue.objects.get(Type=type)
    message = ''
    if queue:
        if switch == 'off':
            queue.isDebug = False
            queue.save()
            message = 'Task debug is suspended'
        else:
            queue.isDebug = True
            queue.save()
            message = 'Task debug is running'
        return HttpResponse(message)
    else:
        return HttpResponse('Task Scheduler does not exist')


class correlationConnectivityThread(threading.Thread):
    """
    开启线程，检查 correlation connectivity preprocessing task 列表中是否存在静态或动态脑连接的计算任务
    """

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print(
            "-----Start Thread for ：Correlation Connectivity Preprocessing         ")
        CorrelationConnectivityPreprocessing.checkTaskStatus()


class causalityConnectivityThread(threading.Thread):
    """
    开启线程，检查 causality connectivity preprocessing task 列表中是否存在GC或NC的脑连接的计算任务
    """

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("-----Start Thread for ：Causality Connectivity Preprocessing")
        CausalityConnectivityPreprocessing.checkTaskStatus()


def ScheduleTasks():
    """
    从任务队列 TaskQueue 中定时执行任务
    :return:
    """
    global ScheduleTasks_start
    if ScheduleTasks_start:
        return
    ScheduleTasks_lock.acquire()
    ScheduleTasks_start = True
    ScheduleTasks_lock.release()
    info = '\n=============================================Current time: ' + datetime.datetime.now(
        pytz.timezone('PRC')).strftime(
        "%Y-%m-%d %H:%M") + '======================================='
    logging.info(info)
    # print('\n=============================================Current time: ' + datetime.datetime.now(
    #     pytz.timezone('PRC')).strftime(
    #     "%Y-%m-%d %H:%M") + '=======================================')
    tasks = TaskQueue.objects.all()
    for task in tasks:
        if task.Type == 'CorrelationConnectivity' and task.isScheduled:
            CorrelationConnectivityPreprocessing.checkTaskStatus()
            task = TaskQueue.objects.get(Type='CorrelationConnectivity')
            task.Task_LastRunTime = timezone.now()
            task.save()
            # thread = correlationConnectivityThread()
            # thread.setDaemon(True)
            # thread.start()
            # threads.append(thread)
        elif task.Type == 'CausalityConnectivity' and task.isScheduled:
            CausalityConnectivityPreprocessing.checkTaskStatus()
            task = TaskQueue.objects.get(Type='CausalityConnectivity')
            task.Task_LastRunTime = timezone.now()
            task.save()
            # thread = causalityConnectivityThread()
            # thread.setDaemon(True)
            # thread.start()
            # threads.append(thread)
    info = '\n========================================Scheduler Finished=================================\n'
    logging.info(info)
    # print('\n========================================Scheduler Finished=================================\n')
    ScheduleTasks_lock.acquire()
    ScheduleTasks_start = False
    ScheduleTasks_lock.release()

    return


job_threading_lock = threading.Lock()
job_is_start = False

ScheduleTasks_lock = threading.Lock()
ScheduleTasks_start = False

# 定时任务中设定多线程会出问题，线程未结束，而由开启下一个任务，执行顺序可能出错。这里还是使用单线程调度
if job_is_start is False:
    sched = BackgroundScheduler()
    sched.add_job(ScheduleTasks, trigger='interval', max_instances=1, seconds=120)
    sched.start()
    job_threading_lock.acquire()
    job_is_start = True
    job_threading_lock.release()
