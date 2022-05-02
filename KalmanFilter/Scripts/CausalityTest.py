from numpy.dual import pinv, det
from numpy.ma import mean, var
from statsmodels.tsa.stattools import grangercausalitytests
import numpy as np


def SearchForOptimalAIC(TwoColumnsSeries, maxlag):
    min_AIC = optimalLag = 10000
    for lag in range(1, maxlag + 1):
        AIC_temp = AIC(TwoColumnsSeries, lag)
        if AIC_temp < min_AIC:
            min_AIC = AIC_temp
            optimalLag = lag
    return min_AIC, optimalLag


def AIC(TwoColumnsSeries, order):
    samples = TwoColumnsSeries.shape[0]
    inChannel_1 = TwoColumnsSeries[:, 0].T
    inChannel_2 = TwoColumnsSeries[:, 1].T
    M1 = M2 = np.zeros((samples - order, order * 2))
    for i in range(order+1, samples+1):
        M1[i - order - 1, :] = np.hstack((inChannel_1[i - order - 1: i - 1], inChannel_2[i - order - 1: i - 1]))
        M2[i - order - 1, :] = np.hstack((inChannel_2[i - order - 1: i - 1], inChannel_1[i - order - 1: i - 1]))
    y1 = inChannel_1[order:].T
    y2 = inChannel_2[order:].T

    coef_1 = pinv(M1.T.dot(M1)).dot(M1.T.dot(y1))
    coef_2 = pinv(M2.T.dot(M2)).dot(M2.T.dot(y2))

    delt_1 = M1.dot(coef_1) - inChannel_1[order:].T
    delt_2 = M2.dot(coef_2) - inChannel_2[order:].T

    Mc = np.cov(delt_1, delt_2)
    AIC_value = samples * np.log(det(Mc)) + 2 * order * 4
    return AIC_value


def GrangerSignificanceTest(TwoColumnsSeries, optimalLag):
    return grangercausalitytests(TwoColumnsSeries, [optimalLag], verbose=False)


def GrangerValueCompute(TwoColumnsSeries, order):
    # joint model
    samples = TwoColumnsSeries.shape[0]
    inChannel_1 = TwoColumnsSeries[:, 0].T
    inChannel_2 = TwoColumnsSeries[:, 1].T
    M1 = M2 = np.zeros((samples - order, order * 2))
    for i in range(order+1, samples+1):
        M1[i - order - 1, :] = np.hstack((inChannel_1[i - order - 1: i - 1], inChannel_2[i - order - 1: i - 1]))
        M2[i - order - 1, :] = np.hstack((inChannel_2[i - order - 1: i - 1], inChannel_1[i - order - 1: i - 1]))
    y1 = inChannel_1[order:].T
    y2 = inChannel_2[order:].T

    coef_1 = pinv(M1.T.dot(M1)).dot(M1.T.dot(y1))
    coef_2 = pinv(M2.T.dot(M2)).dot(M2.T.dot(y2))

    delt_1 = M1.dot(coef_1) - inChannel_1[order:].T
    delt_2 = M2.dot(coef_2) - inChannel_2[order:].T

    # AR model
    M1_AR = M2_AR = np.zeros((samples - order, order))
    for i in range(order + 1, samples + 1):
        M1_AR[i - order - 1, :] = inChannel_1[i - order - 1: i - 1]
        M2_AR[i - order - 1, :] = inChannel_2[i - order - 1: i - 1]
    y1_AR = inChannel_1[order:].T
    y2_AR = inChannel_2[order:].T

    coef_1_AR = pinv(M1_AR.T.dot(M1_AR)).dot(M1_AR.T.dot(y1_AR))
    coef_2_AR = pinv(M2_AR.T.dot(M2_AR)).dot(M2_AR.T.dot(y2_AR))

    delt_1_AR = M1_AR.dot(coef_1_AR) - inChannel_1[order:].T
    delt_2_AR = M2_AR.dot(coef_2_AR) - inChannel_2[order:].T

    GC_2To1 = np.log(var(delt_1_AR) / var(delt_1))
    GC_1To2 = np.log(var(delt_2_AR) / var(delt_2))
    return GC_2To1


def NewCausalityValueCompute(TwoColumnsSeries, order):
    samples = TwoColumnsSeries.shape[0]
    inChannel_1 = TwoColumnsSeries[:, 0].T
    inChannel_2 = TwoColumnsSeries[:, 1].T
    M1 = M2 = np.zeros((samples - order, order * 2))
    for i in range(order+1, samples+1):
        M1[i - order - 1, :] = np.hstack((inChannel_1[i - order - 1: i - 1], inChannel_2[i - order - 1: i - 1]))
        M2[i - order - 1, :] = np.hstack((inChannel_2[i - order - 1: i - 1], inChannel_1[i - order - 1: i - 1]))
    y1 = inChannel_1[order:].T
    coef_1 = pinv(M1.T.dot(M1)).dot(M1.T.dot(y1))
    delt_1 = M1.dot(coef_1) - inChannel_1[order:].T

    M1_2 = M1[:, order:]
    M1_1 = M1[:, 0:order - 1]
    Channel_2InChannel_1Part = M1_2.dot(coef_1[order:])
    Channel_2InChannel_1PartSquareSum = Channel_2InChannel_1Part.T.dot(Channel_2InChannel_1Part)
    Channel_1InChannel_1Part = M1_1.dot(coef_1[0:order - 1])
    Channel_1InChannel_1PartSquareSum = Channel_1InChannel_1Part.T.dot(Channel_1InChannel_1Part)

    # Channel 2 to Channel 1
    NC_BToA = Channel_2InChannel_1PartSquareSum / (
            Channel_1InChannel_1PartSquareSum + Channel_2InChannel_1PartSquareSum + (samples) * var(delt_1))

    return NC_BToA
