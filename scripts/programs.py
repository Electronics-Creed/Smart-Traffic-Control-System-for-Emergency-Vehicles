# import packages
import os
from utils.traffic_system import TrafficSignal
from utils.filter import Filter
from utils.spectrogram import Spectrogram
from utils.emergency_vehicle_detector import EmergencyVehicle
from utils.find_direction import Direction
from utils.Pi import PiControl

PATH = os.getcwd()  # path of current working directory

NUM_TRAFFIC_LIGHTS = 4  # number of traffic lights in the traffic signal
initial_state = [False for _ in range(NUM_TRAFFIC_LIGHTS)]  # initial state of traffic signal
initial_state[0] = True

# pins used in raspberry Pi
RED_LED_PINS = [6, 13, 19, 26]
GREEN_LED_PINS = [12, 16, 20, 21]

ANGLE_ERROR = 1  # error acceptance in angle

# creating objects to access all the functions
obj_spectrogram = Spectrogram()
obj_EVD = EmergencyVehicle(os.path.join(PATH, 'model.h5'), os.path.join(PATH, 'model_weights.h5'))
obj_direction = Direction()
obj_filter = Filter(os.path.join(PATH, 'band_pass1.mat'), os.path.join(PATH, 'band_pass2.mat'))
obj_pi = PiControl(RED_LED_PINS, GREEN_LED_PINS, num_mics=2)
obj_traffic_signal = TrafficSignal(initial_state, NUM_TRAFFIC_LIGHTS)
obj_pi.get_audio_signals()  # get some audio data before starting the traffic signal
obj_pi.get_audio_signals()

print('[BOOTING] starting traffic lights')

while True:  # main while loop
    obj_pi.get_audio_signals()  # get audio signal
    spectrograms = obj_spectrogram.get_spectrograms(obj_pi.signals)  # create spectrograms
    predictions = obj_EVD.emergency_vehicle_detection(spectrograms)
    if True in predictions:  # check if siren is detected
        print('[STATE: DETECTED]', 'Counter:', obj_traffic_signal.counter, 'State:', obj_traffic_signal.state)
        filtered_signals = obj_filter.get_filtered_signals(obj_pi.signals)  # filter the signals
        angle = obj_direction.calculate_angle(filtered_signals)  # calculate the direction

        if angle < 15:  # emergency vehicle entering the traffic signal from left
            obj_traffic_signal.change_state([True, False, False, False])  # change the state
            obj_pi.change_lights(obj_traffic_signal.state, NUM_TRAFFIC_LIGHTS=4)  # change the traffic lights

            print('[TRACKING] emergency vehicle entering the traffic signal')
            while abs(angle - 90) < ANGLE_ERROR:
                pass
            print('[TRACKING] emergency vehicle at the centre of traffic signal')
            while abs(angle - 165) < ANGLE_ERROR:
                pass
            print('[TRACKING] emergency vehicle has left the traffic signal')
            obj_traffic_signal.change_state([False, True, False, False])  # switch back to ready state

        elif angle > 165:  # emergency vehicle entering the traffic signal from right
            obj_traffic_signal.change_state([False, False, True, False])  # change the state
            obj_pi.change_lights(obj_traffic_signal.state, NUM_TRAFFIC_LIGHTS=4)  # change the traffic lights

            print('[TRACKING] emergency vehicle entering the traffic signal')
            while abs(angle - 90) < ANGLE_ERROR:
                pass
            print('[TRACKING] emergency vehicle at the centre of traffic signal')
            while abs(angle - 15) < ANGLE_ERROR:
                pass
            print('[TRACKING] emergency vehicle has left the traffic signal')
            obj_traffic_signal.change_state([False, False, False, True])  # switch back to ready state

    else:
        obj_traffic_signal.if_change_state()  # check if state has to change
        obj_traffic_signal.counter += 1  # increase counter
        print('[STATE: NORMAL]', 'Counter:', obj_traffic_signal.counter, 'State:', obj_traffic_signal.state)
    obj_pi.change_lights(obj_traffic_signal.state, NUM_TRAFFIC_LIGHTS=4)  # change the color of LEDs

obj_pi.end()
