import json
import os.path
import re
import sys
import logging
import logging.config
import time
import threading
import paramiko

# fileName = 'ADNI3_002_S_0413.zip'
fileName = ''
fmriName = ''
TE1 = 0
TE2 = 0
subjectid = ''
hasFieldmap = 0

root_path = ""


# for field map
def Field_Maping_Preprocess(workingPath):
    logging.info('---------------------------')
    logging.info('start Fieldmap re-structure')
    global TE1, TE2
    os.chdir(workingPath + os.listdir(workingPath)[0])
    if len(os.listdir(os.getcwd())) == 2:
        parentFolder = os.getcwd()
        for folder in os.listdir(parentFolder):
            os.chdir(parentFolder + '/' + folder)
            pattern = re.compile(r'^\d+')
            # if file exists, delete it first.
            for file in os.listdir(os.getcwd()):
                if re.findall(pattern, file):
                    command = 'rm -rf ' + file
                    os.system(command)
            command = "dcm2niix -b y -f '%t_%p_%s'  ./"
            os.system(command)
            logging.info('dcm2niix complete')
            pattern = re.compile(r'^\d+')
            for file in os.listdir(os.getcwd()):
                if re.findall(pattern, file):

                    pattern_e1_json = re.compile(r'_e1.json$')
                    if re.findall(pattern_e1_json, file):
                        with open(file, 'r') as load_f:
                            dic = json.load(load_f)
                            if dic['EchoTime']:
                                TE1 = float(dic['EchoTime'])

                            else:
                                logging.error('No EchoTime filed found in ' + file)
                                exit(1)
                        command = 'mv ' + file + ' ' + root_path + '/fmriprep/input/sub-' + str(
                            subjectid) + '/fmap/sub-' + str(subjectid) + '_magnitude1.json'
                        os.system(command)
                    pattern_e1_nii = re.compile(r'_e1.nii$')
                    if re.findall(pattern_e1_nii, file):
                        command = 'mv ' + file + ' ' + root_path + '/fmriprep/input/sub-' + str(
                            subjectid) + '/fmap/sub-' + str(subjectid) + '_magnitude1.nii'
                        os.system(command)
                    pattern_e2_json = re.compile(r'_e2.json$')
                    if re.findall(pattern_e2_json, file):
                        with open(file, 'r') as load_f:
                            dic = json.load(load_f)
                            if dic['EchoTime']:
                                TE2 = float(dic['EchoTime'])
                                load_f.close()
                            else:
                                load_f.close()
                                logging.error('No EchoTime filed found in ' + file)
                                exit(1)
                        command = 'mv ' + file + ' ' + root_path + '/fmriprep/input/sub-' + str(
                            subjectid) + '/fmap/sub-' + str(subjectid) + '_magnitude2.json'
                        os.system(command)
                    pattern_e2_nii = re.compile(r'_e2.nii$')
                    if re.findall(pattern_e2_nii, file):
                        command = 'mv ' + file + ' ' + root_path + '/fmriprep/input/sub-' + str(
                            subjectid) + '/fmap/sub-' + str(subjectid) + '_magnitude2.nii'
                        os.system(command)
                    pattern_ph_json = re.compile(r'_ph.json$')
                    if re.findall(pattern_ph_json, file):
                        with open(file, 'r') as load_f:
                            dic = json.load(load_f)
                            load_f.close()
                            dic['EchoTime1'] = str(TE1)
                            dic['EchoTime2'] = str(TE2)
                            dic['IntendedFor'] = fmriName
                        with open(file, 'w') as load_f:
                            json.dump(dic, load_f)
                            load_f.close()
                        command = 'mv ' + file + ' ' + root_path + '/fmriprep/input/sub-' + str(
                            subjectid) + '/fmap/sub-' + str(subjectid) + '_phasediff.json'
                        os.system(command)
                    pattern_ph_nii = re.compile(r'_ph.nii$')
                    if re.findall(pattern_ph_nii, file):
                        command = 'mv ' + file + ' ' + root_path + '/fmriprep/input/sub-' + str(
                            subjectid) + '/fmap/sub-' + str(subjectid) + '_phasediff.nii'
                        os.system(command)

    logging.info('end Fieldmap re-structure')
    return


# for T1w
def Accelerated_Sagittal_MPRAG(workingPath):
    logging.info('---------------------------')
    logging.info('start T1w re-structure')
    os.chdir(workingPath + os.listdir(workingPath)[0])

    parentFolder = os.getcwd()
    index = 0
    if len(os.listdir(parentFolder)) != 1:
        for folder in os.listdir(parentFolder):
            index = index + 1
            os.chdir(parentFolder + '/' + folder)
            pattern = re.compile(r'^\d+')
            # if file exists, delete it first.
            for file in os.listdir(os.getcwd()):
                if re.findall(pattern, file):
                    command = 'rm -rf ' + file
                    os.system(command)
            command = "dcm2niix -b y -f '%t_%p_%s'  ./"
            os.system(command)
            logging.info('dcm2niix complete')
            pattern = re.compile(r'^\d+')
            for file in os.listdir(os.getcwd()):
                if re.findall(pattern, file):
                    pattern_ph_json = re.compile(r'.json$')
                    if re.findall(pattern_ph_json, file):
                        command = 'mv ' + file + ' ' + root_path + '/fmriprep/input/sub-' + str(
                            subjectid) + '/anat/sub-' + str(subjectid) + '_run-' + str(index) + '_T1w.json'
                        os.system(command)
                    pattern_ph_nii = re.compile(r'.nii$')
                    if re.findall(pattern_ph_nii, file):
                        file_T1w = root_path + '/fmriprep/input/sub-' + str(
                            subjectid) + '/anat/sub-' + str(subjectid) + '_run-' + str(index) + '_T1w.nii'
                        command = 'mv ' + file + ' ' + file_T1w
                        os.system(command)
                        command = 'cp ' + file_T1w + ' ' + root_path + '/freesurfer/input/sub-' + str(subjectid)
                        os.system(command)
    else:
        for folder in os.listdir(parentFolder):

            os.chdir(parentFolder + '/' + folder)
            pattern = re.compile(r'^\d+')
            # if file exists, delete it first.
            for file in os.listdir(os.getcwd()):
                if re.findall(pattern, file):
                    command = 'rm -rf ' + file
                    os.system(command)
            command = "dcm2niix -b y -f '%t_%p_%s'  ./"
            os.system(command)
            logging.info('dcm2niix complete')
            pattern = re.compile(r'^\d+')
            for file in os.listdir(os.getcwd()):
                if re.findall(pattern, file):
                    pattern_ph_json = re.compile(r'.json$')
                    if re.findall(pattern_ph_json, file):
                        command = 'mv ' + file + ' ' + root_path + '/fmriprep/input/sub-' + str(
                            subjectid) + '/anat/sub-' + str(subjectid) + '_T1w.json'
                        os.system(command)
                    pattern_ph_nii = re.compile(r'.nii$')
                    if re.findall(pattern_ph_nii, file):
                        file_T1w = root_path + '/fmriprep/input/sub-' + str(
                            subjectid) + '/anat/sub-' + str(subjectid) + '_T1w.nii'
                        command = 'mv ' + file + ' ' + file_T1w
                        os.system(command)
                        command = 'cp ' + file_T1w + ' ' + root_path + '/freesurfer/input/sub-' + str(subjectid)
                        os.system(command)

    logging.info('end T1w re-structure')
    return


# for fMRI
def Axial_rsfMRI__Eyes_Open(workingPath):
    logging.info('---------------------------')
    logging.info('start fMRI re-structure')
    global fmriName
    os.chdir(workingPath + os.listdir(workingPath)[0])
    if len(os.listdir(os.getcwd())) == 1:
        parentFolder = os.getcwd()
        for folder in os.listdir(parentFolder):
            os.chdir(parentFolder + '/' + folder)
            pattern = re.compile(r'^\d+')
            # if file exists, delete it first.
            for file in os.listdir(os.getcwd()):
                if re.findall(pattern, file):
                    command = 'rm -rf ' + file
                    os.system(command)
            command = "dcm2niix -b y -f '%t_%p_%s'  ./"
            os.system(command)
            logging.info('dcm2niix complete')
            pattern = re.compile(r'^\d+')
            for file in os.listdir(os.getcwd()):
                if re.findall(pattern, file):
                    pattern_ph_json = re.compile(r'.json$')
                    if re.findall(pattern_ph_json, file):
                        command = 'mv "' + file + '" ' + root_path + '/fmriprep/input/sub-' + str(
                            subjectid) + '/func/sub-' + str(subjectid) + '_task-rest_bold.json'
                        os.system(command)
                    pattern_ph_nii = re.compile(r'.nii$')
                    if re.findall(pattern_ph_nii, file):
                        fmriName = root_path + '/fmriprep/input/sub-' + str(subjectid) + '/func/sub-' + str(
                            subjectid) + '_task-rest_bold.nii'
                        command = 'mv "' + file + '" ' + fmriName
                        fmriName = fmriName.split('/')[-1]
                        print(fmriName)
                        os.system(command)

    logging.info('end fMRI re-structure')
    return


def DoFreeSurfer():
    logging.info('---------------------------')
    logging.info('start Freesurfer preprocess for T1w reconstruction')
    # remember to source freesurfer home, find for recon-all command
    time_start = time.time()
    if os.path.exists(root_path + 'freesurfer/output/sub-' + str(subjectid)):
        command = 'rm -rf ' + root_path + 'freesurfer/output/sub-' + str(subjectid)
        os.system(command)
    if os.path.exists('/usr/local/freesurfer/subjects/sub-' + str(subjectid)):
        command = 'rm -rf /usr/local/freesurfer/subjects/sub-' + str(subjectid)
        os.system(command)
    if len(os.listdir(root_path + '/freesurfer/input/sub-' + subjectid)) == 1:
        command = 'source $FREESURFER_HOME/SetUpFreeSurfer.sh && recon-all -s ' + root_path + '/freesurfer/output/' + 'sub-' + str(
            subjectid) + ' -i ' + root_path + '/freesurfer/input/sub-' + subjectid + '/sub-' + str(
            subjectid) + '_T1w.nii -all'
    else:
        index = 1
        command = 'source $FREESURFER_HOME/SetUpFreeSurfer.sh && recon-all -s ' + root_path + '/freesurfer/output/' + 'sub-' + str(
            subjectid)
        for folder in os.listdir(root_path + '/freesurfer/input/sub-' + subjectid):
            command = command + ' -i ' + root_path + '/freesurfer/input/sub-' + subjectid + '/sub-' + str(
                subjectid) + '_run-' + str(index) + '_T1w.nii '
            index = index + 1
        command = command + ' -all'
    os.system(command)
    time_end = time.time()
    logging.info('end Freesurfer preprocess, total time: ' + str((time_end - time_start) / 60 / 60) + 'H')
    command = 'cp -r /usr/local/freesurfer/subjects/sub-' + subjectid + ' ' + root_path + '/freesurfer/output/sub-' + str(
        subjectid)
    os.system(command)
    return


def DoFmriPrep():
    logging.info('---------------------------')
    logging.info('start FmriPrep preprocess for fmri & fieldmap correction')
    time_start = time.time()
    if os.path.exists(root_path + 'fmriprep/output/sub-' + str(subjectid)):
        command = 'rm -rf ' + root_path + 'fmriprep/output/sub-' + str(subjectid)
        os.system(command)
    param = ''
    if hasFieldmap == 1:
        param = ''
    elif hasFieldmap == 0:
        param = '--use-syn-sdc'
    command = 'fmriprep-docker ' + param + ' --fs-license-file /root/projects/freesurfer/license.txt ' + root_path + '/fmriprep/input/' + ' ' + root_path + '/fmriprep/output/ participant --output-space T1w template '
    command = 'docker run --rm -v /root/projects/freesurfer/license.txt:/opt/freesurfer/license.txt:ro ' \
              ' -v ' + root_path + '/fmriprep/input:/data:ro ' \
                                   ' -v ' + root_path + '/fmriprep/output:/out ' \
                                                        ' poldracklab/fmriprep:1.1.1 /data /out participant --output-space T1w template ' + param
    logging.info('Running the following command at: ' + str(time.time()))
    logging.info(command)

    os.system(command)
    time_end = time.time()
    logging.info('end fmriprep preprocess, total time: ' + str((time_end - time_start) / 60 / 60) + 'H')
    logging.info('---------------------------')
    logging.info('Finished all freesurfer and fmriprep process. Please scp all the output into ciftify engine, to '
                 'continue following processes')
    logging.info('---------------------------')
    return


def DoPreprocess():
    global root_path
    global hasFieldmap
    freesurferDir = os.getcwd()
    logDir = '/'.join(str.split('/')[0:6]) + os.sep

    if os.path.exists(os.getcwd() + '/sub-' + subjectid):
        command = 'rm -rf sub-' + subjectid
        os.system(command)
    command = 'unzip -q ' + fileName + ' -d sub-' + subjectid
    os.system(command)
    logging.info('unzip complete')
    os.chdir(os.getcwd() + '/sub-' + subjectid)
    root_path = os.getcwd()

    logging.info('---------------------------')
    logging.info('start preprocessing and restructure foleders in BIDS name conventions.')
    logging.info('subjectID: ' + subjectid)

    subjectDir = os.listdir(os.getcwd() + '/ADNI')

    command = 'mkdir -p fmriprep/input/sub-' + str(subjectid) + '/anat'
    os.system(command)
    command = 'mkdir -p fmriprep/input/sub-' + str(subjectid) + '/fmap'
    os.system(command)
    command = 'mkdir -p fmriprep/input/sub-' + str(subjectid) + '/func'
    os.system(command)
    command = 'mkdir -p freesurfer/input/sub-' + str(subjectid)
    os.system(command)
    command = 'mkdir -p freesurfer/output'
    os.system(command)
    command = 'mkdir -p fmriprep/output'
    os.system(command)

    os.chdir(os.getcwd() + '/ADNI/' + subjectDir[0])
    subdirs = os.listdir(os.getcwd())
    subjectDir = os.getcwd()
    if 'Accelerated_Sagittal_MPRAGE' in subdirs:
        Accelerated_Sagittal_MPRAG(subjectDir + '/Accelerated_Sagittal_MPRAGE/')
    elif 'SAG_MPRAGE_NO_ANGLE' in subdirs:
        Accelerated_Sagittal_MPRAG(subjectDir + '/SAG_MPRAGE_NO_ANGLE/')
    elif 'Accelerated_Sagittal_IR-FSPGR' in subdirs:
        Accelerated_Sagittal_MPRAG(subjectDir + '/Accelerated_Sagittal_IR-FSPGR/')
    elif 'Accelerated_SAG_IR-SPGR' in subdirs:
        Accelerated_Sagittal_MPRAG(subjectDir + '/Accelerated_SAG_IR-SPGR/')
    elif 'Accelerated_Sag_IR-FSPGR' in subdirs:
        Accelerated_Sagittal_MPRAG(subjectDir + '/Accelerated_Sag_IR-FSPGR/')
    elif 'Sagittal_3D_Accelerated_MPRAGE' in subdirs:
        Accelerated_Sagittal_MPRAG(subjectDir + '/Sagittal_3D_Accelerated_MPRAGE/')
    elif 'Sag_Accel_IR-FSPGR' in subdirs:
        Accelerated_Sagittal_MPRAG(subjectDir + '/Sag_Accel_IR-FSPGR/')
    elif 'MPRAGE' in subdirs:
        Accelerated_Sagittal_MPRAG(subjectDir + '/MPRAGE/')
    elif 'MPRAGE_SENSE' in subdirs:
        Accelerated_Sagittal_MPRAG(subjectDir + '/MPRAGE_SENSE/')
    elif 'MPRAGE__NO_ANGLE=' in subdirs:
        Accelerated_Sagittal_MPRAG(subjectDir + '/MPRAGE__NO_ANGLE=/')
    elif 'IR-FSPGR' in subdirs: #2021.05.30 added for GE
        Accelerated_Sagittal_MPRAG(subjectDir + '/IR-FSPGR/')
    else:
        logging.info('Cannot find any T1w DICOMS')
        exit(1)

    if 'Axial_rsfMRI__Eyes_Open_' in subdirs:
        Axial_rsfMRI__Eyes_Open(subjectDir + '/Axial_rsfMRI__Eyes_Open_/')
    elif 'Axial_MB_rsfMRI__Eyes_Open_' in subdirs:
        Axial_rsfMRI__Eyes_Open(subjectDir + '/Axial_MB_rsfMRI__Eyes_Open_/')
    elif 'Axial_rsfMRI__EYES_OPEN_' in subdirs:
        Axial_rsfMRI__Eyes_Open(subjectDir + '/Axial_rsfMRI__EYES_OPEN_/')
    elif 'Axial_rsfMRI__Eyes_Open__Phase_Direction_P_A' in subdirs:
        Axial_rsfMRI__Eyes_Open(subjectDir + '/Axial_rsfMRI__Eyes_Open__Phase_Direction_P_A/')
    elif 'Axial_fcMRI__Eyes_Open_' in subdirs:
        Axial_rsfMRI__Eyes_Open(subjectDir + '/Axial_fcMRI__Eyes_Open_/')
    elif 'Axial_fcMRI__EYES_OPEN_' in subdirs:
        Axial_rsfMRI__Eyes_Open(subjectDir + '/Axial_fcMRI__EYES_OPEN_/')
    elif 'Axial MB rsfMRI (Eyes Open)' in subdirs:
        Axial_rsfMRI__Eyes_Open(subjectDir + '/Axial MB rsfMRI (Eyes Open)/')
    elif 'Axial RESTING fcMRI (EYES OPEN)' in subdirs:
        Axial_rsfMRI__Eyes_Open(subjectDir + '/Axial RESTING fcMRI (EYES OPEN)/')
    elif 'Axial_RESTING_fcMRI__EYES_OPEN_' in subdirs:
        Axial_rsfMRI__Eyes_Open(subjectDir + '/Axial_RESTING_fcMRI__EYES_OPEN_/')
    elif 'Resting_State_fMRI' in subdirs:
        Axial_rsfMRI__Eyes_Open(subjectDir + '/Resting_State_fMRI/')
    elif 'Extended_Resting_State_fMRI' in subdirs:
        Axial_rsfMRI__Eyes_Open(subjectDir + '/Extended_Resting_State_fMRI/')
    elif 'Extended_Resting_State_fMRI_CLEAR' in subdirs:
        Axial_rsfMRI__Eyes_Open(subjectDir + '/Extended_Resting_State_fMRI_CLEAR/')
    # elif 'ASL_PERFUSION' in subdirs:
    #     Axial_rsfMRI__Eyes_Open(subjectDir + '/ASL_PERFUSION/')
    elif 'MoCoSeries' in subdirs:
        Axial_rsfMRI__Eyes_Open(subjectDir + '/MoCoSeries/')
    else:
        logging.info('Cannot find any fmri DICOMs')
        exit(1)

    if 'Field_Mapping' in subdirs:
        hasFieldmap = 1
        Field_Maping_Preprocess(subjectDir + '/Field_Mapping/')
    else:
        hasFieldmap = 0
        logging.info('No fieldmap used for susceptibility correction')

    thread1 = myThread('Freesurfer')
    thread2 = myThread('FmriPrep')

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    #
    logging.info('All processes have finished.')
    # with open(logDir + 'freesurfer.log', 'a') as f:
    #     f.write('All processes have finished.')
    return


class myThread(threading.Thread):  # threading.Thread
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):  # run run
        print("Starting " + self.name)
        if self.name == 'Freesurfer':
            DoFreeSurfer()
        elif self.name == "FmriPrep":
            DoFmriPrep()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        fileName = sys.argv[1]
    if os.path.exists(fileName):
        os.chdir('/'.join(fileName.split('/')[0:-1]))
        if os.path.splitext(fileName)[1] == '.zip':
            pattern = re.search(r'metadata', fileName)
            if pattern is None:
                file = os.path.splitext(fileName)[0].split('/')[-1]
                subjectid = ''.join(file.split('_'))
                logging.basicConfig(level=logging.DEBUG,
                                    format='[%(asctime)s]  %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S',
                                    filename=subjectid + '.log',
                                    filemode='w')
                DoPreprocess()
            else:
                print("Please input image file, not the meta data or others\nfor example: ADNI3_002_S_0413.zip")
                exit(1)
        else:
            print("Please input the zip file downloaded from ADNI3 Database \nfor example: ADNI3_002_S_0413.zip")
            exit(1)
    else:
        print(
            'File ' + fileName + ' does not exist in this folder. \nPlease put this pyscript into the data folder which contains zip files downloaded from ADNI3 database')
        exit(1)
