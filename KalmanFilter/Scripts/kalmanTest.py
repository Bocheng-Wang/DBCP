# coding: utf-8
import numpy
import numpy as np
import pylab
import matplotlib
from nibabel import cifti2
import pandas as pd


def Filter(Series_Base, Series_Ref, AR_model_or_Joint_R_modal):
    SeriesA = _Filter(Series_Base, Series_Ref, AR_model_or_Joint_R_modal)
    SeriesB = _Filter(Series_Ref, Series_Base, AR_model_or_Joint_R_modal)
    return SeriesA, SeriesB

def _Filter(Series_Base, Series_Ref, AR_model_or_Joint_R_modal):
    # 0 for AR, 1 for Joint Regression
    AR_model_or_Joint_R_modal = AR_model_or_Joint_R_modal

    Volume_Length = Series_Base.shape[0]
    sz = (2, Volume_Length)  # size of array

    Observation_Self = Series_Base  # Area #0 fMRI data
    Observation_Reference = Series_Ref  # Other area  fMRI data
    z = numpy.array([Observation_Self, Observation_Reference])

    # allocate space for arrays
    Posteri_estimate = numpy.zeros(sz)  # a posteri estimate of x
    Posteri_error = numpy.zeros(sz)  # a posteri error estimate
    Priori_estimate = numpy.zeros(sz)  # a priori estimate of x
    Priori_error = numpy.zeros(sz)  # a priori error estimate
    K = numpy.zeros(sz)  # gain or blending factor

    if AR_model_or_Joint_R_modal == 0:
        # AR modal
        H = numpy.array([[1, 0], [0, 0]])
        A = numpy.array([[1, 0], [0, 0]])
        Posteri_estimate[:] = numpy.nanmean(z[0, :])
        R = 0.001  # estimate of measurement variance, change to see effect
        Q = 1e-5  # process variance

    elif AR_model_or_Joint_R_modal == 1:
        # Joint VAR modal
        H = numpy.array([[1, 1], [1, 1]])
        A = numpy.array([[1, 1], [1, 1]])
        Posteri_estimate[:, 0] = [700, 760]
        R = 0.000001  # estimate of measurement variance, change to see effect
        Q = 1e-5  # process variance

    for t in range(1, Volume_Length):
        # time update
        # X(k|k-1) = AX(k-1|k-1) + BU(k) + W(k), BU(k) = 0
        Priori_estimate[:, t] = A.dot(Posteri_estimate[:, t - 1])

        # # P(k|k-1) = AP(k-1|k-1)A' + Q(k)
        Priori_error[:, t] = A.dot(Posteri_error[:, t - 1]).dot(A.T) + Q

        # et = Z(k) - HX(k|k-1)
        et = z[:, t] - H.dot(Priori_estimate[:, t])

        # Rt = (1-λ) * R(t-1) + λ * et *et   (Havlicek et al. 2010 NeuroImage, Eq.13)
        # lamda = 0.9
        # R = (1 - lamda) * R + lamda * et * et
        # measurement update
        # Kg(k)=P(k|k-1)H'/[HP(k|k-1)H' + R]

        K[:, t] = Priori_error[:, t].dot(H.T) / (H.dot(Priori_error[:, t]).dot(H.T) + R)

        # X(k|k) = X(k|k-1) + Kg(k)[et]
        Posteri_estimate[:, t] = Priori_estimate[:, t] + K[0, t] * (et)
        # P(k|k) = (1 - Kg(k)H)P(k|k-1)
        Posteri_error[:, t] = (1 - K[:, t].dot(H)).dot(Priori_error[:, t])
    Base_Filtered = Posteri_estimate[0, :]
    return Base_Filtered
# # write to csv
# data = {}
# data["Observation"] = Observation_Self
# data["Reference"] = Observation_Reference
# data["Observation_Kalman"] = Posteri_estimate[0, :]
# data["Reference_Kalman"] = Posteri_estimate[1, :]
# df = pd.DataFrame(data, columns=['Observation', 'Reference', 'Observation_Kalman', 'Reference_Kalman'])
# df.to_csv('tmp/kalmanData.csv')

# draw curve
#
# matplotlib.rcParams['font.sans-serif'] = ['SimHei']
# pylab.style.use('seaborn-dark-palette')
# pylab.close('all')
# pylab.figure(1)
# # pylab.ylim(685, 780)
# pylab.plot(Observation_Self[:], label='观测值')  # 测量值
# pylab.plot(Observation_Reference[:], label='观测值（参考）')  # 测量值
# pylab.plot(Posteri_estimate[0, :], label='卡尔曼滤波')  # 过滤后的值
