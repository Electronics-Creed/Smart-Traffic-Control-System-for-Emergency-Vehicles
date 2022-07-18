import os
import scipy.signal as sps
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import soundfile

PATH = os.getcwd()
ORIGINAL_DATA_PATH = os.path.join(PATH, 'datasets')
AUDIO_DATA_PATH = os.path.join(PATH, 'audio_dataset')
SAMPLE_RATE = 22050

# Start and end times of horn signals
start_time = [0, 0, 1500, 2000, 3000, 0, 0]
end_time = [22000, 9000, 16500, 15000, 22500, 7000, 10000]

i = 0
with os.scandir(ORIGINAL_DATA_PATH) as entries:
    for entry in entries:
        print(entry.name, '->->')
        if 'Car_Horn' in entry.name:
            fs, signal = wavfile.read(os.path.join(ORIGINAL_DATA_PATH, entry.name))
            if signal.size // signal.shape[0] > 1:
                signal = signal[:, 0]
            signal = signal[start_time[i]:end_time[i]]
            i += 1
            # wavfile.write(AUDIO_DATA_PATH + "Car_Honk" + str(i) + ".wav", SAMPLE_RATE, signal.astype(np.int16))
            plt.plot(signal)
            plt.show()
        else:
            try:  # Convert 24-bit to 16-bit signal
                fs, signal = wavfile.read(os.path.join(ORIGINAL_DATA_PATH, entry.name))
            except ValueError:
                soundfile.write(AUDIO_DATA_PATH + entry.name, signal, SAMPLE_RATE, subtype='PCM_16')
                fs, signal = wavfile.read(os.path.join(AUDIO_DATA_PATH, entry.name))  # Get the 16-bit signal
            if signal.size // signal.shape[0] > 1:
                signal = signal[:, 0]
        if fs != SAMPLE_RATE:
            signal = sps.resample(signal, round(len(signal) * SAMPLE_RATE / fs))
        wavfile.write(AUDIO_DATA_PATH + entry.name, SAMPLE_RATE, signal.astype(np.int16))
        print(fs, entry.name)

