import os
import sys
import logging
import logging.config
# from mlab.releases import R2017b as matlab
import time
import matlab.engine




rootDir = ''
fileName = ''
file = ''
subjectid = 'ADNI3002S0413'

def check_folders():
    logging.info('---------------------------')
    logging.info('start checking whether exist folders created before...')
    # check existing folders created before
    subjectDir = '/root/projects/ciftify/ciftify_output/sub-' + subjectid
    if os.path.exists(subjectDir):
        command = 'rm -rf ' + subjectDir
        os.system(command)

    subjectDir_fmri = '/root/projects/ciftify/ciftify_output/qc_fmri/sub-' + subjectid + "_ses-01_task-rest_run-01"
    if os.path.exists(subjectDir_fmri):
        command = 'rm -rf ' + subjectDir_fmri
        os.system(command)

    subjectDir_recon = '/root/projects/ciftify/ciftify_output/qc_recon_all/sub-' + subjectid
    if os.path.exists(subjectDir_recon):
        command = 'rm -rf ' + subjectDir_recon
        os.system(command)
    logging.info('end checking')
    # end check existing folders created before


def Do_CIFTI():
    logging.info('---------------------------')
    logging.info('start cifti_recon_all process')
    freesurfer = rootDir + '/freesurfer/output/'
    command = 'ciftify_recon_all --ciftify-work-dir /root/projects/ciftify/ciftify_output/ --fs-subjects-dir ' + freesurfer + ' sub-' + subjectid
    os.system(command)
    logging.info('end cifti_recon_all process')

    logging.info('start cifti_vis_recon_all process')
    command = 'cifti_vis_recon_all subject --ciftify-work-dir /root/projects/ciftify/ciftify_output/ sub-' + subjectid + \
              ' && cifti_vis_recon_all index --ciftify-work-dir /root/projects/ciftify/ciftify_output/'
    os.system(command)
    logging.info('end cifti_vis_recon_all process')

    logging.info('start cifti_subject_fmri process')
    command = 'ciftify_subject_fmri --ciftify-work-dir /root/projects/ciftify/ciftify_output/ ' + rootDir + '/fmriprep/output/fmriprep/sub-' + subjectid + \
              '/func/sub-' + subjectid + '_task-rest_bold_space-T1w_preproc.nii.gz sub-' + subjectid + ' ses-01_task-rest_run-01'
    os.system(command)
    logging.info('end cifti_subject_fmri process')

    logging.info('start cifti_vis_fmri process')
    command = 'cifti_vis_fmri subject --ciftify-work-dir /root/projects/ciftify/ciftify_output/ ses-01_task-rest_run-01  sub-' + subjectid + \
              ' && cifti_vis_fmri index --ciftify-work-dir /root/projects/ciftify/ciftify_output/'
    os.system(command)
    logging.info('end cifti_vsi_fmri_process')


def Do_HCP_Process():
    logging.info('---------------------------')
    logging.info('start HCP parcellation and correlation process')

    HCP_DIR = rootDir + '/HCP/'
    if os.path.exists(HCP_DIR):
        os.system('rm -rf ' + HCP_DIR)
    command = 'mkdir -p ' + HCP_DIR
    os.system(command)

    # parcellation
    command = 'wb_command -cifti-parcellate  /root/projects/ciftify/ciftify_output/sub-' + subjectid + '/MNINonLinear/Results/ses-01_task-rest_run-01/ses-01_task-rest_run-01_Atlas_s0.dtseries.nii /root/projects/ciftify/HCP_MMP_parcellation.dlabel.nii COLUMN ' + HCP_DIR + 'sub-' + subjectid + '.ptseries.nii'
    os.system(command)
    # correlation between 360 areas
    command = 'wb_command -cifti-correlation ' + HCP_DIR + 'sub-' + subjectid + '.ptseries.nii ' + HCP_DIR + 'sub-' + subjectid + '.pconn.nii'
    os.system(command)
    logging.info('end HCP process. Results are stored in ' + HCP_DIR)


def Do_Matlab():
    logging.info('---------------------------')
    logging.info('start extract correlation matrix into matlab format')
    eng = matlab.engine.start_matlab()
    eng.addpath(eng.genpath(r'/root/projects/ciftify/'))
    print(rootDir + '/HCP/sub-' + subjectid + '.pconn.nii')
    print(rootDir + '/HCP/sub-' + subjectid + '.mat')
    eng.ciftiopen(rootDir + '/HCP/sub-' + subjectid + '.pconn.nii', rootDir + '/HCP/sub-' + subjectid + '.mat', 'wb_command')
    logging.info('end matlab extraction')


def Do_CP():
    logging.info('---------------------------')
    logging.info('start cp files')
    command = 'cp -r ' + rootDir + '/HCP/* ' + rootDir

    os.system(command)
    command = 'rm -rf ' + rootDir + '/HCP '+ rootDir +'/ADNI ' + rootDir + '/fmriprep ' + rootDir + '/freesurfer'

    os.system(command)
    command = 'cp -r /root/projects/ciftify/ciftify_output/sub-' + subjectid + '/* ' + rootDir

    os.system(command)
    command = 'rm -rf /root/projects/ciftify/ciftify_output/sub-' + subjectid

    os.system(command)





if __name__ == "__main__":
    if len(sys.argv) == 2:
        rootDir = os.getcwd()
        fileName = os.path.split(sys.argv[1])[1]
        file = fileName.split('.')[0]
        subjectid = ''.join(file.split('_'))
        rootDir = rootDir + '/sub-' + subjectid

        logging.basicConfig(level=logging.DEBUG,
                            format='[%(asctime)s]  %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename= subjectid + '.log',
                            filemode='a')

        check_folders()
        timestart = time.time()
        Do_CIFTI()
        timeend = time.time()
        logging.info('CIFTIFY duration: ' + str((timeend - timestart)/60%60) + 'H')

        timestart = time.time()
        Do_HCP_Process()
        Do_Matlab()
        Do_CP()
        timeend = time.time()
        logging.info('HCP correlation and parcellation process duration: ' + str((timeend - timestart) % 60) + ' min')
        logging.info('Finished all process without error')





