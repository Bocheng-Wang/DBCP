# coding: utf-8
import sys
import threading
import time

import numpy
import numpy as np
from nibabel import cifti2
# from CausalityTest import *
import CausalityTest, kalmanTest
import scipy.io as io

import urllib.parse
import urllib.request
import logging

# AR_modal_GC_matrix_RAW = numpy.zeros((360, 360))
# AR_modal_NC_matrix_RAW = numpy.zeros((360, 360))

# Kalman filtered
JAR_modal_GC_matrix_Sig_Kalman = numpy.zeros((360, 360))
JAR_modal_NC_matrix_Sig_Kalman = numpy.zeros((360, 360))
Correlation_matrix_Kalman = numpy.zeros((360, 360))

# without Kalman filtered
JAR_modal_GC_matrix_Sig_no_Kalman = numpy.zeros((360, 360))
JAR_modal_NC_matrix_Sig_no_Kalman = numpy.zeros((360, 360))
Correlation_matrix_no_Kalman = numpy.zeros((360, 360))


def saveMatrix(taskDir):
    """
    Folder Structure:
    -------Causality/
    ----------------Scripts/
    ----------------Original/
    ----------------Results/
    :return:
    """
    global JAR_modal_GC_matrix_Sig_Kalman, JAR_modal_NC_matrix_Sig_Kalman
    global JAR_modal_GC_matrix_Sig_no_Kalman, JAR_modal_NC_matrix_Sig_no_Kalman

    io.savemat(taskDir + 'Results/JAR_modal_GC_matrix_Sig_Kalman.mat', {'Results': JAR_modal_GC_matrix_Sig_Kalman})
    io.savemat(taskDir + 'Results/JAR_modal_NC_matrix_Sig_Kalman.mat', {'Results': JAR_modal_NC_matrix_Sig_Kalman})
    io.savemat(taskDir + 'Results/JAR_modal_GC_matrix_Sig_no_Kalman.mat',
               {'Results': JAR_modal_GC_matrix_Sig_no_Kalman})
    io.savemat(taskDir + 'Results/JAR_modal_NC_matrix_Sig_no_Kalman.mat',
               {'Results': JAR_modal_NC_matrix_Sig_no_Kalman})
    io.savemat(taskDir + 'Results/Correlation_matrix_Kalman.mat', {'Results': Correlation_matrix_Kalman})
    io.savemat(taskDir + 'Results/Correlation_matrix_no_Kalman.mat', {'Results': Correlation_matrix_no_Kalman})


def getMatrix(area_Base):
    global JAR_modal_GC_matrix_Sig_Kalman, JAR_modal_NC_matrix_Sig_Kalman
    global JAR_modal_GC_matrix_Sig_no_Kalman, JAR_modal_NC_matrix_Sig_no_Kalman
    global Correlation_matrix_no_Kalman, Correlation_matrix_Kalman
    global PSeries
    for ref_area_index in range(area_Base, 360):
        Observation_Self = PSeries[:, area_Base]  # Area #0 fMRI data
        Observation_Reference = PSeries[:, ref_area_index]  # Other area  fMRI data
        # print("    Start   Area_Base：" + str(area_Base) + '---vs.---Area_Ref:' + str(ref_area_index))

        # JAR modal with Kalman
        [f_value_B2A, GC_BToA, NC_BToA], [f_value_A2B, GC_AToB, NC_AToB], Correlation = PairwiseCausality(
            Observation_Self,
            Observation_Reference,
            modal=1, Kalman=True)
        JAR_modal_GC_matrix_Sig_Kalman[area_Base, ref_area_index] = GC_BToA
        JAR_modal_NC_matrix_Sig_Kalman[area_Base, ref_area_index] = NC_BToA
        JAR_modal_GC_matrix_Sig_Kalman[ref_area_index, area_Base] = GC_AToB
        JAR_modal_NC_matrix_Sig_Kalman[ref_area_index, area_Base] = NC_AToB
        Correlation_matrix_Kalman[area_Base, ref_area_index] = Correlation
        Correlation_matrix_Kalman[ref_area_index, area_Base] = Correlation

        # JAR modal without Kalman
        [f_value_B2A, GC_BToA, NC_BToA], [f_value_A2B, GC_AToB, NC_AToB], Correlation = PairwiseCausality(
            Observation_Self,
            Observation_Reference,
            modal=1, Kalman=False)
        JAR_modal_GC_matrix_Sig_no_Kalman[area_Base, ref_area_index] = GC_BToA
        JAR_modal_NC_matrix_Sig_no_Kalman[area_Base, ref_area_index] = NC_BToA
        JAR_modal_GC_matrix_Sig_no_Kalman[ref_area_index, area_Base] = GC_AToB
        JAR_modal_NC_matrix_Sig_no_Kalman[ref_area_index, area_Base] = NC_AToB
        Correlation_matrix_no_Kalman[area_Base, ref_area_index] = Correlation
        Correlation_matrix_no_Kalman[ref_area_index, area_Base] = Correlation


def PairwiseCausality(Observation_Self, Observation_Reference, modal, Kalman):
    # return: f_value_A2B, f_value_B2A

    if Kalman:
        SeriesA, SeriesB = kalmanTest.Filter(Observation_Self, Observation_Reference, modal)
    else:
        SeriesA = Observation_Self
        SeriesB = Observation_Reference

    ## B2A Test
    TwoColumnsSeries = np.vstack((SeriesA.T, SeriesB.T)).T
    # Search For the minimal AIC and optimal Lag
    min_AIC, optimalLag = CausalityTest.SearchForOptimalAIC(TwoColumnsSeries, maxlag=30)
    # Granger  Significance  Test
    # 有些fMRI采样较少，比如只有54个volume，granger中对lag有个判断，大致是满足：数据点是lag长度的三倍以上。
    try:
        result = CausalityTest.GrangerSignificanceTest(TwoColumnsSeries, optimalLag)
    except:
        result = CausalityTest.GrangerSignificanceTest(TwoColumnsSeries, 12)
    f_value_B2A = [value[0]['ssr_ftest'][1] for value in result.values()][0]
    GC_BToA = NC_BToA = 0
    if f_value_B2A <= 0.05:
        # Granger Value Compute
        GC_BToA = CausalityTest.GrangerValueCompute(TwoColumnsSeries, order=optimalLag)
        NC_BToA = CausalityTest.NewCausalityValueCompute(TwoColumnsSeries, order=optimalLag)

    ## A2B Test
    TwoColumnsSeries = np.vstack((SeriesB.T, SeriesA.T)).T
    # Search For the minimal AIC and optimal Lag
    min_AIC, optimalLag = CausalityTest.SearchForOptimalAIC(TwoColumnsSeries, maxlag=30)
    # Granger  Significance  Test
    try:
        result = CausalityTest.GrangerSignificanceTest(TwoColumnsSeries, optimalLag)
    except:
        result = CausalityTest.GrangerSignificanceTest(TwoColumnsSeries, 12)
    f_value_A2B = [value[0]['ssr_ftest'][1] for value in result.values()][0]
    GC_AToB = NC_AToB = 0
    if f_value_A2B <= 0.05:
        # Granger Value Compute
        GC_AToB = CausalityTest.GrangerValueCompute(TwoColumnsSeries, order=optimalLag)
        # New Causality Value Compute
        NC_AToB = CausalityTest.NewCausalityValueCompute(TwoColumnsSeries, order=optimalLag)

    Correlation = np.corrcoef(TwoColumnsSeries.T)
    result = [f_value_B2A, GC_BToA, NC_BToA], [f_value_A2B, GC_AToB, NC_AToB], Correlation[0, 1]

    return result


PSeries = []


def postMessage(UUID, type):
    if type == 'Success':
        response = urllib.request.urlopen('http://dbcp.cuz.edu.cn/KalmanFilter/SuccessOnRemoteCompute/' + UUID,
                                          timeout=5)
        response.read()

    elif type == 'Failed':
        response = urllib.request.urlopen('http://dbcp.cuz.edu.cn/KalmanFilter/FailInRemoteCompute/' + UUID, timeout=5)
        response.read()


if __name__ == "__main__":
    #
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
        UUID = fileName.split('/')[-3]

        taskDir = '/root/projects/DataForPreprocess/Causality/' + UUID + '/'

        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                            filename=taskDir + 'log.txt')
        # try:
            #                 BOLD = cifti2.cifti2.load('../tmp/average.tmp.ptseries.nii')
        BOLD = cifti2.cifti2.load(fileName)

        PSeries = BOLD.get_fdata()  # 140 x 360 parcellated fMRI data

        for base_area_index in range(0, 360):
            logging.info("Start  Area_Base：" + str(base_area_index))
            getMatrix(base_area_index)
            logging.info("End    Area_Base：" + str(base_area_index))
        saveMatrix(taskDir=taskDir)
        postMessage(UUID=UUID, type='Success')
        # except:
        #     postMessage(UUID=UUID, type='Failed')
    else:
        print('arguments not satisfied. Should be python CausalityAnalysisMain.py filepath')
