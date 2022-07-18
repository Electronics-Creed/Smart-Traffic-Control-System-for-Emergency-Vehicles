# import packages
import numpy as np
import matplotlib.pyplot as plt


class Spectrogram:
    def __init__(self):
        self.NO_OVERLAP = 84  # Overlap for continuous FFT
        self.SAMPLE_FREQ = 22050  # sampling frequency
        self.INTERVAL = 3  # 3 second audio interval in used

    def get_xn(self, Xs, n):  # calculate the FFT
        L = len(Xs)
        ks = np.arange(0, L, 1)
        xn = np.sum(Xs * np.exp((1j * 2 * np.pi * ks * n) / L)) / L
        return xn

    def get_xns(self, ts):
        mag = []
        L = len(ts)
        for n in range(int(L / 2)):
            mag.append(np.abs(self.get_xn(ts, n)) * 2)
        return mag

    def get_Hz_scale_vec(self, ks, Npoints):
        freq_Hz = ks * self.SAMPLE_FREQ / Npoints
        freq_Hz = [int(i) for i in freq_Hz]
        return freq_Hz

    def create_spectrogram(self, ts, noverlap=None, NFFT=256):  # generate the spectrogram
        if noverlap is None:  # check if overlap needed
            noverlap = NFFT / 2
        noverlap = int(noverlap)
        starts = np.arange(0, len(ts), NFFT - noverlap, dtype=int)  # get each frame
        starts = starts[starts + NFFT < len(ts)]
        xns = []
        for start in starts:  # calculate the complete FFT of the signal
            ts_window = self.get_xns(ts[start:start + NFFT])
            xns.append(ts_window)
        spec = 10 * np.log10(np.array(xns).T)  # scale using log function
        assert int(spec.shape[1]) == len(starts)  # check the dimensions of spectrogram
        return spec

    def plot_spectrogram(self, spec, ts, L, NFFT=256, noverlap=None, mappable=None):  # plot the spectrogram
        starts = np.arange(0, len(ts), NFFT - noverlap, dtype=int)  # get each frame
        starts = starts[starts + NFFT < len(ts)]
        plt.figure(figsize=(20, 8))
        plt.imshow(spec, origin='lower')
        Nyticks = 10
        ks = np.linspace(0, spec.shape[0], Nyticks)
        ksHz = self.get_Hz_scale_vec(ks, len(ts))
        plt.yticks(ks, ksHz)
        plt.ylabel("Frequency (Hz)")

        Nxticks = 10
        ts_spec = np.linspace(0, spec.shape[1], Nxticks)
        total_ts_sec = len(ts) / self.SAMPLE_FREQ
        ts_spec_sec = ["{:4.2f}".format(i) for i in np.linspace(0, total_ts_sec * starts[-1] / len(ts), Nxticks)]
        plt.xticks(ts_spec, ts_spec_sec)
        plt.xlabel("Time (sec)")

        plt.title("Spectrogram L={} Spectrogram.shape={}".format(L, spec.shape))
        plt.colorbar(mappable, use_gridspec=True)
        plt.show()

    @staticmethod
    def spectrogram_scaling(x, in_min, in_max, out_min=0, out_max=255):  # scale the spectrogram to have values in the range [0, 255]
        spec = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        return spec.astype(np.int16)

    def get_spectrograms(self, sigs):  # generate scaled spectrogram for the audio signals
        specs = self.create_spectrogram(sigs, self.NO_OVERLAP, 256)
        return self.spectrogram_scaling(specs, np.min(specs), np.max(specs))
    
    # def get_spectrograms(self, sigs): # generate scaled spectrograms for all the audio signals
    #    specs = tuple(map(self.create_spectrogram, sigs.T, [self.NO_OVERLAP for _ in range(sigs.shape[1])], [256 for _ in range(sigs.shape[1])]))
    #    return tuple(map(self.spectrogram_scaling, specs, [np.min(specs[i]) for i in range(len(specs))], [np.max(specs[i]) for i in range(len(specs))]))