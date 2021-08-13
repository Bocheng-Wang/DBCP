import math
import os

import nibabel
import numpy
from nibabel import cifti2
import scipy.io as io


def cifti_parcellation(wb_dir, input, label, output):
    wb_command = wb_dir + '  -cifti-parcellate ' + input + ' ' + label + ' COLUMN ' + output
    os.system(wb_command)


def cifti_correlation(wb_dir, input, output):
    wb_command = wb_dir + ' -cifti-correlation ' + input + ' ' + output
    os.system(wb_command)


def segmentInMatlab(workDir, subjectDir, output, subjectID, wbcommand):
    # Load dtseries data into memory
    subject_dir = subjectDir
    cifti_file_dir = workDir + '/ciftify_output/' + subjectID + '/MNINonLinear/Results/ses-01_task-rest_run-01/ses-01_task-rest_run-01_Atlas_s0.dtseries.nii'
    workbench_dir = wbcommand

    # Static Connectivity preparation
    label_dir = workDir + '\HCP_MMP_parcellation.dlabel.nii'
    dtseries_tmp = cifti_file_dir
    ptseries_file_tmp = subject_dir + '/HCP/average.tmp.ptseries.nii'
    print('static cifti parcellation')
    cifti_parcellation(workbench_dir, dtseries_tmp, label_dir, ptseries_file_tmp)
    connection_file_tmp = subject_dir + '/HCP/average_tmp.pconn.nii'
    print('static cifti correlation')
    cifti_correlation(workbench_dir, ptseries_file_tmp, connection_file_tmp)

    # save Static Connectivity
    BOLD = cifti2.cifti2.load(connection_file_tmp)
    conn = BOLD.get_fdata()
    outputfolder = output + 'StaticConnectivity/'
    if not os.path.exists(outputfolder):
        os.system('mkdir -p ' + outputfolder)
    print('static cifti save')
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

        SeriesAxis = cifti2.cifti2_axes.SeriesAxis(0, 0, 15)
        BrainModelAxis = data.header.get_axis(1)
        newheader = cifti2.Cifti2Header.from_axes((SeriesAxis, BrainModelAxis))

        new_img = cifti2.cifti2.Cifti2Image(windowed_dseries.T, header=newheader,
                                            nifti_header=data.nifti_header.copy())
        # new_img.update_headers()
        print('dynamic cifti tmp save TMP nii')
        new_img.to_filename(dtseries_tmp_)
        print(new_img.header.matrix.get_data_shape())
        nn = nibabel.load(dtseries_tmp_)
        print(nn.header.matrix.get_data_shape())

    for windowIndex in range(0, dWin_number):
        label_dir = workDir + '\HCP_MMP_parcellation.dlabel.nii'
        dtseries_tmp_ = '/tmp/' + str(windowIndex) + '.tmp.dtseries.nii'
        ptseries_file_tmp = subject_dir + '/HCP/' + str(windowIndex) + '.tmp.ptseries.nii'
        print('dynamic cifti parcellation')
        cifti_parcellation(workbench_dir, dtseries_tmp_, label_dir, ptseries_file_tmp)
        connection_file_tmp = subject_dir + '/HCP/' + str(windowIndex) + '_tmp.pconn.nii'
        print('dynamic cifti correlation')
        cifti_correlation(workbench_dir, ptseries_file_tmp, connection_file_tmp)
        # save Dynamic Connectivity
        BOLDD = cifti2.cifti2.load(connection_file_tmp)
        connD = BOLDD.get_fdata()
        outputfolder = output + 'DynamicConnectivity/'
        if not os.path.exists(outputfolder):
            os.system('mkdir -p ' + outputfolder)
        io.savemat(outputfolder + str(windowIndex + 1) + '.mat', {'connectivity': connD}, do_compression=True)


# ciftify_rootDir = '/root/projects/DataForPreprocess/Data/90f897d1-c3ed-4dab-8b84-9a984a11c53e/1.ciftify/'
# subjectid = 'ADNI2073S0089'
# subjectDir = ciftify_rootDir + 'ciftify_data/sub-' + subjectid
# rootDir = subjectDir
# outputDir = rootDir + '/Connectivity/'
#
# segmentInMatlab(ciftify_rootDir, rootDir, outputDir, 'sub-' + subjectid, 'wb_command')

win_width = 15
vertex_total = 91282

windowed_dseries = numpy.zeros([vertex_total, win_width])
dtseries_tmp = './new.nii'
data = nibabel.load(dtseries_tmp)
data.header.shape = windowed_dseries.shape
SeriesAxis = cifti2.cifti2_axes.SeriesAxis(0, 0, 15)
BrainModelAxis = data.header.get_axis(1)
newheader = cifti2.Cifti2Header.from_axes((SeriesAxis, BrainModelAxis))

new_img = cifti2.cifti2.Cifti2Image(windowed_dseries.T, header=newheader,
                                    nifti_header=data.nifti_header.copy())
new_img.to_filename('./new.nii')
