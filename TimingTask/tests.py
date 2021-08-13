# from django.test import TestCase
#
# # Create your tests here.
#
# from django.shortcuts import render
#
# # Create your views here.
#
# from apscheduler.schedulers.background import BackgroundScheduler
#
# # 实例化调度器
# import DBCPOnline
# from DBCPOnline import SSHCommand
# from DBCPOnline.ServerManagement import PopAvailableServer, AquireAvailableServer, CheckServerIsBusy
# from DBCPOnline.models import PreprocessTask
# from django.utils import timezone
#
#
# def checkTaskStatus():
#     preprocessTaskList = PreprocessTask.objects.all()
#     for task in preprocessTaskList:
#         if task.Task_Start and not task.Task_Finish:
#             print('------- Found Preprocessing Task  -- ID: ' + str(
#                 task.id) + '  -- Owner: ' + task.Task_Modal.RARFile.uploader.name)
#             updateOwnedTaskProgressValue(task)
#     check_and_submitTask()
#
#
# def check_and_submitTask():
#     server = AquireAvailableServer()
#     if server:
#         preprocessTaskList = PreprocessTask.objects.filter(Task_Start=False)
#         if len(preprocessTaskList):
#             task = preprocessTaskList[0]
#             if task.Task_Server and (task.Preprocess_Type == 'Dynamic'):
#                 busy = CheckServerIsBusy(task.Task_Server)
#                 if busy is False:
#                     toStartPreprocessingTask(task)
#             elif task.Preprocess_Type == 'Static':
#                 task.Task_Server = server
#                 toStartPreprocessingTask(task)
#     return
#
#
#
# print('')
# def toStartPreprocessingTask(task):
#     status = 500
#     try:
#         SSHCommand.toStartThreadinSSH(task)
#         task.Task_StartTime = timezone.now()
#         task.Task_Start = True
#         task.Preprocessed_Dir = '/'.join(
#             task.Task_Modal.RARFile.storage_path.split('/')[0:4]) + '/Preprocessed/' + task.Task_Modal.uuidStr
#         server = task.Task_Server
#         server.Server_IsBusy = True
#         server.save()
#         task.save()
#         status = 200
#     except:
#         status = 500
#         print(
#             'task start with error. Task ID:' + str(task.id) + '   -- Owner: ' + task.Task_Modal.RARFile.uploader.name)
#     return status
#
#
# def updateOwnedTaskProgressValue(task):
#     status = 500
#     progressValue = SSHCommand.lookupLogFilesInSSH(task)['value']
#     task.Progress_value = round(float(progressValue), 2)
#     if progressValue == '100':
#         status = onFinishedPreprocessingTask(task)
#     else:
#         task.save()
#         status = 200
#     return status
#
#
# def onFinishedPreprocessingTask(task):
#     status = 500
#     try:
#         SSHCommand.onFinishThreadinSSH(task)
#         task.Task_Finish = True
#         task.Task_EndTime = timezone.now()
#         if task.Preprocess_Type == 'Static':
#             preprocessTaskList = PreprocessTask.objects.filter(Task_Modal=task.Task_Modal,
#                                                                Preprocess_Type='Dynamic')
#             taskDynamic = preprocessTaskList[0]
#             taskDynamic.Task_Server = task.Task_Server
#             taskDynamic.save()
#
#         PopAvailableServer(task.Task_Server)
#         task.save()
#         status = 200
#     except:
#         status = 500
#         print(
#             'task finish with error. Task ID:' + str(task.id) + '   -- Owner: ' + task.Task_Modal.RARFile.uploader.name)
#     return status
#
#
# sched = BackgroundScheduler()
# print('Timing Task Start')
# sched.add_job(checkTaskStatus, trigger='interval', max_instances=1, seconds=300)
# sched.start()
