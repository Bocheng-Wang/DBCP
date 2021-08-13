import math
import os
import sys
import logging
import logging.config
# from mlab.releases import R2017b as matlab
import time
# import matlab.engine
import nibabel
import numpy
from nibabel import cifti2
import scipy.io as io

ciftify_rootDir = ''
# ciftify_rootDir = '/root/projects/DataForPreprocess/Data/b64fa40c-02c5-11eb-92c1-80006ef1a7ff/1.ciftify/'
fileName = ''
file = ''
rootDir = ''
subjectid = ''


def check_folders():
    logging.info('---------------------------')
    logging.info('start checking whether exist folders created before...')
    # check existing folders created before
    subjectDir = ciftify_rootDir + 'ciftify_output/sub-' + subjectid
    if os.path.exists(subjectDir):
        command = 'rm -rf ' + subjectDir
        os.system(command)

    subjectDir_fmri = ciftify_rootDir + 'ciftify_output/qc_fmri/sub-' + subjectid + "_ses-01_task-rest_run-01"
    if os.path.exists(subjectDir_fmri):
        command = 'rm -rf ' + subjectDir_fmri
        os.system(command)

    subjectDir_recon = ciftify_rootDir + 'ciftify_output/qc_recon_all/sub-' + subjectid
    if os.path.exists(subjectDir_recon):
        command = 'rm -rf ' + subjectDir_recon
        os.system(command)
    logging.info('end checking')
    # end check existing folders created before


def Do_CIFTI():
    logging.info('---------------------------')
    logging.info('start cifti_recon_all process')
    freesurfer = rootDir + '/freesurfer/output/'
    command = 'ciftify_recon_all --ciftify-work-dir ' + ciftify_rootDir + 'ciftify_output/ --fs-subjects-dir ' + freesurfer + ' sub-' + subjectid
    logging.info(command)
    os.system(command)
    logging.info('end cifti_recon_all process')

    logging.info('start cifti_vis_recon_all process')
    command = 'cifti_vis_recon_all subject --ciftify-work-dir ' + ciftify_rootDir + 'ciftify_output/ sub-' + subjectid + \
              ' && cifti_vis_recon_all index --ciftify-work-dir ' + ciftify_rootDir + 'ciftify_output/'
    # os.system(command)
    logging.info('end cifti_vis_recon_all process')

    logging.info('start cifti_subject_fmri process')
    command = 'ciftify_subject_fmri --ciftify-work-dir ' + ciftify_rootDir + 'ciftify_output/ ' + rootDir + '/fmriprep/output/fmriprep/sub-' + subjectid + \
              '/func/sub-' + subjectid + '_task-rest_bold_space-T1w_preproc.nii.gz sub-' + subjectid + ' ses-01_task-rest_run-01'
    os.system(command)
    logging.info('end cifti_subject_fmri process')

    logging.info('start cifti_vis_fmri process')
    command = 'cifti_vis_fmri subject --ciftify-work-dir ' + ciftify_rootDir + 'ciftify_output/ ses-01_task-rest_run-01  sub-' + subjectid + \
              ' && cifti_vis_fmri index --ciftify-work-dir ' + ciftify_rootDir + 'ciftify_output/'
    # os.system(command)
    logging.info('end cifti_vsi_fmri_process')


def Do_CP():
    logging.info('---------------------------')
    logging.info('start cp files')
    # command = 'cp -r ' + rootDir + '/HCP/* ' + rootDir
    # os.system(command)

    # command = 'rm -rf ' + rootDir + '/HCP ' + rootDir + '/ADNI ' + rootDir + '/fmriprep ' + rootDir + '/freesurfer'
    # os.system(command)

    command = 'cp -r ' + ciftify_rootDir + 'ciftify_output/sub-' + subjectid + '/* ' + rootDir
    os.system(command)

    command = 'rm -rf ' + ciftify_rootDir + 'ciftify_output/sub-' + subjectid
    os.system(command)


def cifti_parcellation(wb_dir, input, label, output):
    wb_command = wb_dir + '  -cifti-parcellate ' + input + ' ' + label + ' COLUMN ' + output
    os.system(wb_command)


def cifti_correlation(wb_dir, input, output):
    wb_command = wb_dir + ' -cifti-correlation ' + input + ' ' + output
    os.system(wb_command)


def segmentNotInMatlab(workDir, subjectDir, output, subjectID, wbcommand):
    # Load dtseries data into memory
    subject_dir = subjectDir
    cifti_file_dir = workDir + '/ciftify_output/' + subjectID + '/MNINonLinear/Results/ses-01_task-rest_run-01/ses-01_task-rest_run-01_Atlas_s0.dtseries.nii'
    workbench_dir = wbcommand

    # Static Connectivity preparation
    label_dir = workDir + '\HCP_MMP_parcellation.dlabel.nii'
    dtseries_tmp = cifti_file_dir
    ptseries_file_tmp = subject_dir + '/HCP/average.tmp.ptseries.nii'
    cifti_parcellation(workbench_dir, dtseries_tmp, label_dir, ptseries_file_tmp)
    connection_file_tmp = subject_dir + '/HCP/average_tmp.pconn.nii'
    cifti_correlation(workbench_dir, ptseries_file_tmp, connection_file_tmp)

    # save Static Connectivity
    BOLD = cifti2.cifti2.load(connection_file_tmp)
    conn = BOLD.get_fdata()
    outputfolder = output + 'StaticConnectivity/'
    if not os.path.exists(outputfolder):
        os.system('mkdir -p ' + outputfolder)
    io.savemat(outputfolder + 'staticConnectivity.mat', {'connectivity': conn}, do_compression=True)

    # Dynamic Connectivity preparation
    BOLD = cifti2.cifti2.load(cifti_file_dir)
    dense_timeseries = BOLD.get_fdata().T
    fMRIVolumns_number = dense_timeseries.shape[1]  # ??? 91282 x 105
    step = 1
    win_width = 15
    vertex_total = 91282

    dWin_number = math.floor((fMRIVolumns_number - win_width) / step)
    for windowIndex in range(0, dWin_number):
        windowed_dseries = numpy.zeros([vertex_total, win_width])
        start_point = step * (windowIndex)
        windowed_dseries[:, :] = dense_timeseries[:, start_point: start_point + win_width]

        dtseries_tmp_ = '/tmp/' + str(windowIndex) + '.tmp.dtseries.nii'
        # for nibabel, columns are parcels which do not match the requirement of HCP Pipeline command
        # In HCP wb_command, columns are volumes, rows are parcels in dtseries.nii file
        data = nibabel.load(dtseries_tmp)
        data.header.shape = windowed_dseries.shape

        SeriesAxis = cifti2.cifti2_axes.SeriesAxis(0, 0, 15)
        BrainModelAxis = data.header.get_axis(1)
        newheader = cifti2.Cifti2Header.from_axes((SeriesAxis, BrainModelAxis))

        new_img = cifti2.cifti2.Cifti2Image(windowed_dseries.T, header=newheader,
                                            nifti_header=data.nifti_header.copy())
        # new_img.update_headers()
        new_img.to_filename(dtseries_tmp_)
    for windowIndex in range(0, dWin_number):
        label_dir = workDir + '\HCP_MMP_parcellation.dlabel.nii'
        dtseries_tmp_ = '/tmp/' + str(windowIndex) + '.tmp.dtseries.nii'
        ptseries_file_tmp = subject_dir + '/HCP/' + str(windowIndex) + '.tmp.ptseries.nii'
        cifti_parcellation(workbench_dir, dtseries_tmp_, label_dir, ptseries_file_tmp)
        connection_file_tmp = subject_dir + '/HCP/' + str(windowIndex) + '_tmp.pconn.nii'
        cifti_correlation(workbench_dir, ptseries_file_tmp, connection_file_tmp)
        # save Dynamic Connectivity
        BOLDD = cifti2.cifti2.load(connection_file_tmp)
        connD = BOLDD.get_fdata()
        outputfolder = output + 'DynamicConnectivity/'
        if not os.path.exists(outputfolder):
            os.system('mkdir -p ' + outputfolder)
        io.savemat(outputfolder + str(windowIndex + 1) + '.mat', {'connectivity': connD}, do_compression=True)


def Do_Segment_Parcellation_Process():
    logging.info('---------------------------')
    logging.info('start HCP parcellation and correlation process')

    HCP_DIR = rootDir + '/HCP/'
    if os.path.exists(HCP_DIR):
        os.system('rm -rf ' + HCP_DIR)
    command = 'mkdir -p ' + HCP_DIR
    os.system(command)

    outputDir = rootDir + '/Connectivity/'

    segmentNotInMatlab(ciftify_rootDir, rootDir, outputDir, 'sub-' + subjectid, 'wb_command')
    logging.info('end HCP parcellation and correlation process')

# Usage:
# python  1.ciftify.py subjectID  ciftifyFoloder_in_subjectDir
# Example cmd:
# python /root/projects/DataForPreprocess/Scripts/1.ciftify.py ADNI2_002_S_0295 /root/projects/DataForPreprocess/Data/b64fa40c-02c5-11eb-92c1-80006ef1a7ff/1.ciftify/

if __name__ == "__main__":
    if len(sys.argv) == 3:
        os.chdir(sys.argv[2])
        ciftify_rootDir = sys.argv[2]
        subjectID = sys.argv[1]
        subjectid = ''.join(subjectID.split('_'))
        subjectDir = sys.argv[2] + 'ciftify_data/sub-' + subjectid
        rootDir = subjectDir
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(asctime)s]  %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=subjectDir + '/' + subjectid + '.log',
                            filemode='a')

        check_folders()
        timestart = time.time()
        Do_CIFTI()
        timeend = time.time()
        logging.info('CIFTIFY duration: ' + str((timeend - timestart) / 60 % 60) + 'H')

        timestart = time.time()
        Do_Segment_Parcellation_Process()
        Do_CP()
        timeend = time.time()
        logging.info('HCP correlation and parcellation process duration: ' + str((timeend - timestart) % 60) + ' min')
        logging.info('Finished all process without error')
