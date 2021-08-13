# coding=utf-8
import os
import tempfile

from django.conf import settings

from DBCP_Scheduler.models import CorrelationConnectivityTask, CausalityConnectivityTask
import logging


def executeCMD(cmd):
    # logging.info(cmd)
    # print(cmd)
    result = os.system(cmd)
    if not result:
        # logging.info('\033[1;34m ---Execution in SSH OK-- \033[0m')
        # print('Execution in SSH OK')
        return 200
    else:
        logging.info(cmd)
        logging.info('\033[1;33m -------Something wrong----- \033[0m')
        logging.error(result)
        # print('\033[0;35;46m ----Something wrong----- \033[0m')
        return 500


def toStartParcellationAndCorrelationInSSH(task):
    """
    Start Parcellation and Correlation preprocessing in SSH
    :param task:
    :return: 200:success, 500 failed
    """
    status = 200
    rootDir = '/root/projects/DataForPreprocess/'
    Data_Dir = rootDir + 'Data/'
    Script_Dir = rootDir + 'Scripts/'
    UUID_Dir = Data_Dir + task.Task_Modal.uuidStr + '/'
    if task.Preprocess_Type == 'Static':
        # mkdir according to Modal`s UUID
        command = 'ssh root@' + task.Task_Server.Server_IP + ' mkdir ' + UUID_Dir
        executeCMD(command)

        # cp example folders into UUID
        command = 'ssh root@' + task.Task_Server.Server_IP + ' cp -r ' + '/root/projects/DataForPreprocess/BaseFolder/* ' + UUID_Dir
        executeCMD(command)

        filename = ''.join(task.Task_Modal.RARFile.filename.split('_')[0:4]) + '.zip'
        # cp subject.zip into UUID
        command = 'scp  root@' + task.Task_Modal.RARFile.storage_path + ' root@' + task.Task_Server.Server_IP + ':' + UUID_Dir + '0.freesurfer/' + filename
        executeCMD(command)

        # cp scripts to server
        local_Scripts = '/var/www/DBCP.Web/DBCPOnline/Script/*'
        command = 'scp -r ' + local_Scripts + ' root@' + task.Task_Server.Server_IP + ':' + '/root/projects/DataForPreprocess/Scripts/'
        executeCMD(command)

        # run nohup see https://www.cnblogs.com/liangblog/p/12762674.html
        command = 'ssh root@' + task.Task_Server.Server_IP + ' \'nohup python -u ' + Script_Dir + '0.run.py ' + UUID_Dir + '0.freesurfer/' + filename + ' > ' + UUID_Dir + 'freesurfer.log 2>&1 &\''
        logging.info(command)
        result = os.system(command)
        if not result:
            logging.info('OK')
        else:
            logging.error(result)
            status = 500
        return status
    elif task.Preprocess_Type == 'Dynamic':
        command = 'ssh root@' + task.Task_Server.Server_IP + ' \'nohup python -u ' + Script_Dir + '2.auto1.py -D ' + UUID_Dir + ' > ' + UUID_Dir + 'ciftify.log 2>&1 &\''
        logging.info(command)
        result = os.system(command)
        if not result:
            return 200
        else:
            logging.error(result)
            return 500


def toDeleteParcellationAndCorrelationPreprocessFolderInSSH(task):
    rootDir = '/root/projects/DataForPreprocess/'
    Data_Dir = rootDir + 'Data/'
    Script_Dir = rootDir + 'Scripts/'
    UUID_Dir = Data_Dir + task.Task_Modal.uuidStr + '/'
    if task.Preprocess_Type == 'Static':
        if task.Task_Start:
            if task.Task_Server:
                command = 'ssh root@' + task.Task_Server.Server_IP + ' rm -rf ' + UUID_Dir
                executeCMD(command)

    elif task.Preprocess_Type == 'Dynamic':
        DBCPStorageIP = settings.CUSTOM_SETTINGS['DBCP.Storage.Server']
        command = 'ssh root@' + DBCPStorageIP + ' rm -rf /' + '/'.join(
            task.Task_Modal.RARFile.storage_path.split('/')[1:])
        executeCMD(command)
        if task.Task_Finish:
            command = 'ssh root@' + DBCPStorageIP + ' rm -rf /' + '/'.join(
                task.Task_Modal.RARFile.storage_path.split('/')[1:4]) + '/Preprocessed/' + task.Task_Modal.uuidStr
            executeCMD(command)

    return


def onFinishParcellationAndCorrelationinSSH(task):
    """
    parcellated and correlation folders here to be moved, stored and cleaned
    :param task:
    :return:
    """

    rootDir = '/root/projects/DataForPreprocess/'
    Data_Dir = rootDir + 'Data/'
    Script_Dir = rootDir + 'Scripts/'
    UUID_Dir = Data_Dir + task.Task_Modal.uuidStr + '/'
    if task.Preprocess_Type == 'Static':
        # cp fmriprep files into ciftify_data folder
        command = 'ssh root@' + task.Task_Server.Server_IP + ' cp -r ' + UUID_Dir + '0.freesurfer/sub-' + ''.join(
            task.Task_Modal.RARFile.filename.split('_')[0:4]) + ' ' + UUID_Dir + '1.ciftify/ciftify_data/'
        executeCMD(command)
    elif task.Preprocess_Type == 'Dynamic':
        # save matrix
        # 10.1.125.6:/root/DBCP.Data/5.AD/Original/ADNI2_002_S_0295_M06.zip
        command = 'ssh root@' + settings.CUSTOM_SETTINGS['DBCP.Storage.Server'] + ' mkdir -p /' + '/'.join(
            task.Task_Modal.RARFile.storage_path.split('/')[1:4]) + '/Preprocessed/' + task.Task_Modal.uuidStr
        executeCMD(command)
        command = 'ssh root@' + task.Task_Server.Server_IP + ' scp -r ' + UUID_Dir + '1.ciftify/ciftify_data/sub-' + ''.join(
            task.Task_Modal.RARFile.filename.split('_')[0:4]) + ' ' + 'root@' + '/'.join(
            task.Task_Modal.RARFile.storage_path.split('/')[0:4]) + '/Preprocessed/' + task.Task_Modal.uuidStr
        executeCMD(command)
        command = 'ssh root@' + task.Task_Server.Server_IP + ' rm -rf ' + UUID_Dir
        executeCMD(command)
        # To restart Server. Due to the 'defunct' threads may exist
        # By this, task may be assigned failed. But it is OK. Scheduler would cancel the failed task and reset server till it is assigned correctly
        # RestartServer(task.Task_Server.Server_IP)
        task.AfterPreprocessed_Saved_Dir = '/'.join(
            task.Task_Modal.RARFile.storage_path.split('/')[0:4]) + '/Preprocessed/'
    return 200


def CheckParcellationThreadInServer(IP):
    """

    :param IP:
    :return: 200:success, -1 failed
    """

    with tempfile.TemporaryDirectory() as tempDir:
        tempDir = tempDir + os.sep
        command = 'ssh root@' + IP + ' ps -ef | grep python > ' + tempDir + 'remoteServerStatus.txt'
        executeCMD(command)

        status = -1
        freesurferString = '0.run.py'
        ciftifyString = '2.auto1.py'
        try:
            with open(tempDir + 'remoteServerStatus.txt', 'r') as f:
                for line in f:
                    if line.find(freesurferString) != -1 or line.find(ciftifyString) != -1:
                        status = 200
                        return status
        except:
            return -1
        if status == -1:
            return status


def CleanUpParcellationServer(Server):
    """
    #??????????????????????
    :param IP:
    :return:
    """
    command = 'ssh root@' + Server.Server_IP + ' mv /root/projects/DataForPreprocess/Data/fmriprep_for_analysis/ /root/projects/DataForPreprocess/'
    executeCMD(command)

    command = 'ssh root@' + Server.Server_IP + ' rm -rf /root/projects/DataForPreprocess/Data/*'
    executeCMD(command)

    command = 'ssh root@' + Server.Server_IP + ' mv /root/projects/DataForPreprocess/fmriprep_for_analysis /root/projects/DataForPreprocess/Data'
    executeCMD(command)


def CleanUpCausalityServer(Server):
    """
    #??????????????????????
    :param IP:
    :return:
    """
    command = 'ssh root@' + Server.Server_IP + ' rm -rf /root/projects/DataForPreprocess/Causality/*'
    executeCMD(command)


def CancelCausalityServerTask(Server):
    with tempfile.TemporaryDirectory() as tempDir:
        tempDir = tempDir + os.sep
        command = 'ssh root@' + Server.Server_IP + ' pgrep python > ' + tempDir + 'remoteThreadID.txt'
        executeCMD(command)
        status = -1
        try:
            with open(tempDir + 'remoteThreadID.txt', 'r') as f:
                for line in f:
                    threadID = line
                    command = 'ssh root@' + Server.Server_IP + ' kill ' + threadID
                    executeCMD(command)
        except:
            return -1
        if status == -1:
            return status


def lookupParcellationAndCorrelationLogFilesInSSH(task):
    """
    Check Parcellation and Correlation local log files
    :param task:
    :return:{'status': 200, 'value': rate} {'status': 500, 'value': 0}
    """
    with tempfile.TemporaryDirectory() as tempDir:
        tempDir = tempDir + os.sep
        subjectStr = ''.join(task.Task_Modal.RARFile.filename.split('_')[0:4])
        subjectDir = '/root/projects/DataForPreprocess/Data/' + task.Task_Modal.uuidStr + '/'
        remote_freesurferLog = subjectDir + 'freesurfer.log'
        remote_ciftifyLog = subjectDir + '1.ciftify/ciftify_data/sub-' + subjectStr + '/' + subjectStr + '.log'
        local_freesurferLog = tempDir + task.Task_Modal.uuidStr + '.freesurfer.log'
        local_ciftifyLog = tempDir + task.Task_Modal.uuidStr + '.ciftify.log'

        remote_Runlog = subjectDir + '0.freesurfer/*.log'
        local_Runlog = tempDir + task.Task_Modal.uuidStr + '.run.log'
        if task.Preprocess_Type == 'Static':
            command = 'scp root@' + task.Task_Server.Server_IP + ':' + remote_freesurferLog + ' ' + local_freesurferLog
            executeCMD(command)
            command = 'scp root@' + task.Task_Server.Server_IP + ':' + remote_Runlog + ' ' + local_Runlog
            executeCMD(command)
        elif task.Preprocess_Type == 'Dynamic':
            command = 'scp root@' + task.Task_Server.Server_IP + ':' + remote_ciftifyLog + ' ' + local_ciftifyLog
            executeCMD(command)

        if task.Preprocess_Type == 'Static':
            freesurfer_count = -1
            freesurfer_finish = False

            # I dont know which freesurfer or fmriprep stops first
            finalString = 'Finished all freesurfer and fmriprep'
            finalString = 'All processes have finished.'
            freesurfer_count = 0
            try:
                with open(tempDir + task.Task_Modal.uuidStr + '.freesurfer.log', 'rU') as f:
                    for line in f:
                        freesurfer_count += 1
                        # if line.find(finalString) != -1:
                        #     freesurfer_finish = True
                with open(tempDir + task.Task_Modal.uuidStr + '.run.log', 'rU') as f:
                    for line in f:
                        if line.find(finalString) != -1:
                            freesurfer_finish = True
            except:
                return {'status': 200, 'value': 0}

            # for freesurfer_count, line in enumerate(
            #         open(tempDir + task.Task_Modal.uuidStr + '.freesurfer.log', 'rU')):
            #     freesurfer_count += 1
            #     if line.find(finalString) != -1:
            #         freesurfer_finish = True
            rate = freesurfer_count / 11729 * 100
            if freesurfer_finish:
                rate = '100'
        elif task.Preprocess_Type == 'Dynamic':
            ciftify_count = -1
            ciftify_finish = False
            finalString = 'Finished all process without error'
            ciftify_count = 0
            try:
                with open(tempDir + task.Task_Modal.uuidStr + '.ciftify.log', 'rU') as f:
                    for line in f:
                        ciftify_count += 1
                        if line.find(finalString) != -1:
                            ciftify_finish = True
            except:
                return {'status': 200, 'value': 0}
            # for ciftify_count, line in enumerate(
            #         open(tempDir + task.Task_Modal.uuidStr + '.ciftify.log', 'rU')):
            #     ciftify_count += 1
            #     if line.find(finalString) != -1:
            #         ciftify_finish = True
            rate = ciftify_count / 60 * 100
            if ciftify_finish:
                rate = '100'

        return {'status': 200, 'value': rate}


def lookupCausalityLogfileInSSH(task):
    """
    To check causality computation progress value in server-end
    :param task:
    :return:
    """
    with tempfile.TemporaryDirectory() as tempDir:

        rootDir = '/root/projects/DataForPreprocess/'

        # '/root/projects/DataForPreprocess/Causality/'
        Causality_DIR = rootDir + task.Task_Type + os.sep

        # '/root/projects/DataForPreprocess/Causality/UUID/'
        UUID_Dir = Causality_DIR + task.Task_Modal.uuidStr + os.sep

        # '/root/projects/DataForPreprocess/Causality/UUID/log.txt'
        remoteLogPath = UUID_Dir + 'log.txt'

        tempDir = tempDir + os.sep
        local_Log = tempDir + task.Task_Modal.uuidStr + '.log'

        command = 'scp root@' + task.Task_Server.Server_IP + ':' + remoteLogPath + ' ' + local_Log
        executeCMD(command)

        logline_count = 0
        task_finish = False
        finalString = 'End    Area_Base：359'
        try:
            with open(local_Log, 'rU') as f:
                for line in f:
                    logline_count += 1
                    # if line.find(finalString) != -1:
                    #     task_finish = True
        except:
            return {'status': 200, 'value': 0}
        rate = logline_count / 720 * 100
        return {'status': 200, 'value': rate}


def toStartCausalityInSSH(task):
    """
    To assign causality task for server-end
    :param task:Causality Task in which server has been assigned
    :return:
    """
    status = 200
    rootDir = '/root/projects/DataForPreprocess/'

    # '/root/projects/DataForPreprocess/Causality/'
    Causality_DIR = rootDir + task.Task_Type + os.sep

    # '/root/projects/DataForPreprocess/Causality/UUID/'
    UUID_Dir = Causality_DIR + task.Task_Modal.uuidStr + os.sep

    # '/root/projects/DataForPreprocess/Causality/UUID/Script/'
    Script_Dir = UUID_Dir + 'Scripts' + os.sep

    # '/root/projects/DataForPreprocess/Causality/UUID/OriginalData/'
    Data_Dir = UUID_Dir + 'OriginalData' + os.sep

    # '/root/projects/DataForPreprocess/Causality/UUID/Results/'
    Results_Dir = UUID_Dir + 'Results' + os.sep

    # mkdir -p Task Folder to Modal`s UUID
    command = 'ssh root@' + task.Task_Server.Server_IP + ' mkdir -p ' + Script_Dir
    executeCMD(command)
    command = 'ssh root@' + task.Task_Server.Server_IP + ' mkdir -p ' + Data_Dir
    executeCMD(command)
    command = 'ssh root@' + task.Task_Server.Server_IP + ' mkdir -p ' + Results_Dir
    executeCMD(command)

    # cp Storage.Server ptseries.nii folders into UUID
    ptseries_filePath = CorrelationConnectivityTask.objects.filter(Task_Modal=task.Task_Modal)[
                            0].Preprocessed_Dir + '/sub-' + ''.join(
        task.Task_Modal.RARFile.filename.split('_')[0:4]) + '/HCP/average.tmp.ptseries.nii'
    command = 'scp  root@' + ptseries_filePath + ' root@' + task.Task_Server.Server_IP + ':' + Data_Dir
    executeCMD(command)

    # cp scripts to server
    local_Scripts = '/var/www/DBCP.Web/KalmanFilter/Scripts'
    command = 'scp -r ' + local_Scripts + ' root@' + task.Task_Server.Server_IP + ':' + UUID_Dir
    executeCMD(command)

    command = 'ssh root@' + task.Task_Server.Server_IP + ' \'nohup python -u ' + Script_Dir + 'CausalityAnalysisMain.py ' + Data_Dir + 'average.tmp.ptseries.nii ' + ' > ' + UUID_Dir + 'causality.log 2>&1 &\''
    status = executeCMD(command)
    return status


# todo  Test for migration
def MigrateModal(ModalID, toServerIP):
    task = CausalityConnectivityTask.objects.get(Task_Modal_id=ModalID)
    FromServerIP = task.Preprocessed_Dir.split(':')[0]
    Folder = task.Preprocessed_Dir.split(':')[1]
    cmd = 'ssh root@' + FromServerIP + '  scp -r ' + Folder + ' ' + toServerIP + ':' + Folder
    result = executeCMD(cmd)
    if result == 500:
        return 500
    if result == 200:
        task.Preprocessed_Dir = toServerIP + ':' + Folder
        task.AfterPreprocessed_Saved_Dir = toServerIP + ':' + task.AfterPreprocessed_Saved_Dir.split(':')[1]
        task.save()

        tasks = CorrelationConnectivityTask.objects.filter(Task_Modal_id=ModalID)
        for task in tasks:
            task.Preprocessed_Dir = toServerIP + ':' + Folder
            task.AfterPreprocessed_Saved_Dir = toServerIP + ':' + task.AfterPreprocessed_Saved_Dir.split(':')[1]
            task.save()
        return 200


def toDeleteCausalityProgressFolderInSSH(task):
    """
    To delete causality progress folder in SSH
    :param task:
    :param type: settings.Task_Type['Causality']
    :return:
    """
    rootDir = '/root/projects/DataForPreprocess/'

    # '/root/projects/DataForPreprocess/Causality/'
    Causality_DIR = rootDir + task.Task_Type + os.sep

    # '/root/projects/DataForPreprocess/Causality/UUID/'
    UUID_Dir = Causality_DIR + task.Task_Modal.uuidStr + os.sep

    if task.Task_Start:
        command = 'ssh root@' + task.Task_Server.Server_IP + ' rm -rf ' + UUID_Dir
        os.system(command)
    return


def onFinishTaskInSSH(task):
    """
    Task Results folders here to be moved, stored and cleaned
    :param task:
    :param type: settings.Task_Type['Causality']
    :return:
    """
    # /root/projects/DataForPreprocess/Causality/576db552-17e5-4d36-ad42-6e96c46ff481/Origin/
    # /root/projects/DataForPreprocess/Causality/576db552-17e5-4d36-ad42-6e96c46ff481/Result/
    type = task.Task_Type
    rootDir = '/root/projects/DataForPreprocess/'

    # '/root/projects/DataForPreprocess/Causality/'
    Causality_DIR = rootDir + task.Task_Type + os.sep

    # '/root/projects/DataForPreprocess/Causality/UUID/'
    UUID_Dir = Causality_DIR + task.Task_Modal.uuidStr + os.sep

    # '/root/projects/DataForPreprocess/Causality/UUID/Script/'
    Script_Dir = UUID_Dir + 'Scripts' + os.sep

    # '/root/projects/DataForPreprocess/Causality/UUID/OriginalData/'
    Data_Dir = UUID_Dir + 'OriginalData' + os.sep

    # '/root/projects/DataForPreprocess/Causality/UUID/Results/'
    Results_Dir = UUID_Dir + 'Results' + os.sep

    # mkdir on storage server
    command = 'ssh root@' + settings.CUSTOM_SETTINGS['DBCP.Storage.Server'] + ' mkdir -p /' + '/'.join(
        task.Task_Modal.RARFile.storage_path.split('/')[
        1:4]) + '/Preprocessed/' + task.Task_Modal.uuidStr + '/' + type + os.sep
    executeCMD(command)

    # cp results
    command = 'ssh root@' + task.Task_Server.Server_IP + ' scp -r ' + Results_Dir + ' ' + 'root@' + '/'.join(
        task.Task_Modal.RARFile.storage_path.split('/')[
        0:4]) + '/Preprocessed/' + task.Task_Modal.uuidStr + '/' + type + os.sep
    executeCMD(command)

    # delete folders
    command = 'ssh root@' + task.Task_Server.Server_IP + ' rm -rf ' + UUID_Dir
    executeCMD(command)

    task.AfterPreprocessed_Saved_Dir = '/'.join(
        task.Task_Modal.RARFile.storage_path.split('/')[
        0:4]) + '/Preprocessed/' + task.Task_Modal.uuidStr + '/' + type + os.sep
    return


def CheckCausalityThreadInServer(IP):
    with tempfile.TemporaryDirectory() as tempDir:
        tempDir = tempDir + os.sep
        command = 'ssh root@' + IP + ' ps -ef | grep python > ' + tempDir + 'remoteServerStatus.txt'
        executeCMD(command)

        status = -1
        TaskThreadString = 'CausalityAnalysisMain.py'
        try:
            with open(tempDir + 'remoteServerStatus.txt', 'r') as f:
                for line in f:
                    if line.find(TaskThreadString) != -1:
                        status = 200
                        return status
        except:
            return -1
        if status == -1:
            return status


def RestartServer(Server):
    '''
    重启服务器可能导致任务分配失败，直至服务器启动成功
    建议在Parcellation中使用，该进程会启动大量多线程，重启有助于清楚内存等
    而在Causality任务中，使用单线程，重启代价较大，不建议使用。2021.06.08
    :param Server:
    :return:
    '''
    command = 'ssh root@' + Server.Server_IP + ' shutdown -r now'
    executeCMD(command)
