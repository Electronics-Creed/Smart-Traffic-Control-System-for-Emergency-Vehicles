# import packages
import random
import numpy as np
from scipy.io import wavfile
import os
import cv2
import warnings
from utils.spectrogram import Spectrogram

warnings.filterwarnings("ignore", category=RuntimeWarning)

# define paths
PATH = os.getcwd()
AUDIO_DATASET_PATH = os.path.join(PATH, 'audio_dataset')
DATASET_PATH = os.path.join(PATH, 'dataset')

# create directories for dataset
os.mkdir(DATASET_PATH)
for i in ['train', 'validate', 'test']:
    os.mkdir(os.path.join(DATASET_PATH, i))
    for j in ['yes', 'no']:
        os.mkdir(os.path.join(DATASET_PATH, i + '\\' + j))

# get audio dataset
FILES = {'EMERGENCY': [], 'VEHICLE': [], 'NOISE': []}
with os.scandir(AUDIO_DATASET_PATH) as entries:
    for entry in entries:
        if 'Ambulance' in entry.name or 'Police' in entry.name or 'Fire_Truck' in entry.name:
            FILES['EMERGENCY'].append(entry.name)
        elif 'Car_Honk' in entry.name:
            FILES['VEHICLE'].append(entry.name)
        elif 'Traffic_noise' in entry.name:
            FILES['NOISE'].append(entry.name)
        else:
            print('Unknown Type')

INTERVAL = 3  # time interval of each audio signal
num_of_samples = 3000  # total number of spectrograms generated
num_pos_neg_data = [0.6 * num_of_samples, 0.4 * num_of_samples]  # number of positive and negative samples
percentage_split = [0.1, 0.25, 1]  # train, test, validate dataset split
status = 25  # show status of the program
file_number = [0, 0, 0, 0, 0, 0]  # store file number in each directory

obj_spectrogram = Spectrogram()  # create object to generate spectrogram


def get_time(length):  # returns random time in the signal
    return random.randint(0, length)


def get_interval(length, length_clip):  # returns random interval in the signal
    return random.randint(0, length - length_clip)


def get_noise():  # returns random noise signal
    x = get_time(len(noise))
    return np.concatenate((noise[x:], noise[0:x]), axis=0)


def get_siren():  # combines noise and partial siren
    n_signal = get_noise()
    x = get_time(len(emergency))
    n_signal[len(noise) - x - 1: -1] += emergency[0: x]
    return n_signal


def get_siren_noise():  # combines noise and siren
    n_signal = get_noise()

    if len(emergency) > len(noise):
        n_signal = np.concatenate((n_signal, n_signal[0:len(emergency) - len(noise)]), axis=0)
        n_signal += emergency
    elif len(emergency) < len(noise):
        n_signal = emergency + n_signal[0:len(emergency)]
    else:
        n_signal += emergency
    return n_signal


def get_vehicle_noise():  # combines noise and vehicle sounds
    n_signal = get_noise()

    for _ in range(random.randint(0, 3)):  # use different vehicles
        fs_vehicle, vehicle = wavfile.read(os.path.join(AUDIO_DATASET_PATH, random.choice(FILES['VEHICLE'])))
        clip_len = len(vehicle)
        y = get_interval(len(n_signal), clip_len)
        n_signal[y:y + clip_len] += vehicle
    return n_signal


def get_siren_vehicle():  # combines noise sirens and vehicle sounds
    n_signal = get_noise()

    x = get_time(len(emergency))
    n_signal[len(noise) - x - 1: -1] += emergency[0: x]

    for _ in range(random.randint(0, 1)):  # use different vehicles
        fs_vehicle, vehicle = wavfile.read(os.path.join(AUDIO_DATASET_PATH, random.choice(FILES['VEHICLE'])))
        clip_len = len(vehicle)
        y = get_interval(len(n_signal), clip_len)
        n_signal[y:y + clip_len] += vehicle
    return n_signal


def store_data(x):  # to store spectrogram in respective directories
    x += 65
    if x == 65 or x == 67:
        if file_number[0] < percentage_split[0] * num_pos_neg_data[1]:
            cv2.imwrite(os.path.join(DATASET_PATH, 'test\\no\\img' + chr(x) + str(file_number[0]) + '.jpg'), spec)
            file_number[0] += 1
        elif file_number[1] < percentage_split[1] * num_pos_neg_data[1]:
            cv2.imwrite(os.path.join(DATASET_PATH, 'validate\\no\\img' + chr(x) + str(file_number[1]) + '.jpg'), spec)
            file_number[1] += 1
        else:
            cv2.imwrite(os.path.join(DATASET_PATH, 'train\\no\\img' + chr(x) + str(file_number[2]) + '.jpg'), spec)
            file_number[2] += 1
    else:
        if file_number[3] < percentage_split[0] * num_pos_neg_data[0]:
            cv2.imwrite(os.path.join(DATASET_PATH, 'test\\yes\\img' + chr(x) + str(file_number[3]) + '.jpg'), spec)
            file_number[3] += 1
        elif file_number[4] < percentage_split[1] * num_pos_neg_data[0]:
            cv2.imwrite(os.path.join(DATASET_PATH, 'validate\\yes\\img' + chr(x) + str(file_number[4]) + '.jpg'), spec)
            file_number[4] += 1
        else:
            cv2.imwrite(os.path.join(DATASET_PATH, 'train\\yes\\img' + chr(x) + str(file_number[5]) + '.jpg'), spec)
            file_number[5] += 1


for i in range(1, num_of_samples + 1):  #

    # import signals
    fs_noise, noise = wavfile.read(os.path.join(AUDIO_DATASET_PATH, random.choice(FILES['NOISE'])))
    fs_emergency, emergency = wavfile.read(os.path.join(AUDIO_DATASET_PATH, random.choice(FILES['EMERGENCY'])))

    # clip the signals to random 3 seconds
    noise_clip = get_interval(len(noise), INTERVAL * fs_noise)
    noise = 0.5 * noise[noise_clip:noise_clip + INTERVAL * fs_noise]
    emergency_clip = get_interval(len(emergency), INTERVAL * fs_emergency)
    emergency = emergency[emergency_clip:emergency_clip + INTERVAL * fs_emergency]

    # get random combinations of dataset
    x = random.randint(0, 4)
    if x == 0:
        s = get_noise()
    elif x == 1:
        s = get_siren()
    elif x == 2:
        s = get_vehicle_noise()
    elif x == 3:
        s = get_siren_noise()
    else:
        s = get_siren_vehicle()

    spec = obj_spectrogram.get_spectrograms(s)  # generate spectrogram
    store_data(x)  # store spectrogram

    if i % status == 0:  # print status
        print('<-----  ' + str(i) + " images have been stored" + '  ----->')