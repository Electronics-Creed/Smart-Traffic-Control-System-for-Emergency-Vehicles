# import packages
import numpy as np
import scipy.signal as signal
from scipy.fft import fft
import matplotlib.pyplot as plt
from scipy.io import loadmat


class Filter:
    def __init__(self, band_pass1_path, band_pass2_path):
        self.Fs = 22050  # sampling frequency

        # load bandpass filter SOS and gain values
        band_pass1 = loadmat(band_pass1_path)
        self.sos_bp1 = band_pass1['SOS'].copy(order='C')
        self.g_bp1 = band_pass1['G'].copy(order='C')

        band_pass2 = loadmat(band_pass2_path)
        self.sos_bp2 = band_pass2['SOS'].copy(order='C')
        self.g_bp2 = band_pass2['G'].copy(order='C')

    def get_filtered_signal(self, sig):  # filter the signal
        bp1_output = signal.sosfilt(self.sos_bp1, sig) * np.prod(self.g_bp1)
        bp2_output = signal.sosfilt(self.sos_bp2, sig) * np.prod(self.g_bp2)
        return bp1_output + bp2_output

    def get_filtered_signals(self, signals):  # filter multiple signals
        return tuple(map(self.get_filtered_signal, signals.T))

    def plot_filtered_signal(self, sig, interval):  # Plot the filtered signal
        t = np.linspace(0, interval, interval * self.Fs)
        filtered_signal = self.get_filtered_signal(sig)
        fig = plt.figure()
        fig.suptitle('Filter Plots')
        plt.subplot(221)
        plt.title('Input signal')
        plt.xlabel('time')
        plt.ylabel('Amplitude')
        plt.plot(t, sig)
        plt.subplot(222)
        plt.title('FFT of Input signal')
        plt.xlabel('frequency')
        plt.ylabel('Amplitude')
        plt.plot(abs(fft(sig)))
        plt.ylim([0, 4e7])
        plt.subplot(223)
        plt.title('Filtered signal')
        plt.xlabel('time')
        plt.ylabel('Amplitude')
        plt.plot(t, filtered_signal)
        plt.subplot(224)
        plt.title('FFT of Filtered signal')
        plt.xlabel('frequency')
        plt.ylabel('Amplitude')
        plt.plot(abs(fft(filtered_signal)))
        plt.ylim([0, 4e7])
        plt.show()
