# import packages
import sounddevice as sd
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import numpy as np


class PiControl:
    def __init__(self, RED_LED_PINS, GREEN_LED_PINS, num_mics=1):
        GPIO.setmode(GPIO.BCM)  # set the mode to GPIO numbering
        GPIO.setwarnings(False)

        self.RED_LED_PINS = RED_LED_PINS
        self.GREEN_LED_PINS = GREEN_LED_PINS
        # set the LED pins as output pins
        for led_pin in RED_LED_PINS:
            GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)
        for led_pin in GREEN_LED_PINS:
            GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)

        self.Fs = 22050  # sampling frequency
        self.INTERVAL = 3  # audio id recorded for 3 seconds
        self.NUM_MICS = num_mics  # number of mics used
        self.signals = np.zeros((self.INTERVAL * self.Fs, self.NUM_MICS))  # collect the audio

    def change_lights(self, state, NUM_TRAFFIC_LIGHTS):  # change the lights of traffic signal based on state
        for i in range(NUM_TRAFFIC_LIGHTS):
            GPIO.output(self.RED_LED_PINS[i], not state[i])
            GPIO.output(self.GREEN_LED_PINS[i], state[i])

    def get_audio_signal(self, interval=1):  # get audio from one microphone
        signal = sd.rec(int(interval * self.Fs), samplerate=self.Fs, channels=1)  # get one second audio
        sd.wait()
        signal *= 5e3  # amplitude scaling
        self.signals = np.concatenate((self.signals[1 * self.Fs:], signal), axis=None)  # concatenate the audio with previous audio

    def get_audio_signals(self, interval=1, NUM_CHANNELS=2):  # get audio from multiple microphone
        signal = sd.rec(int(interval * self.Fs), samplerate=self.Fs, channels=NUM_CHANNELS)
        sd.wait()
        signal *= 5e3
        for i in range(NUM_CHANNELS):
            self.signals = np.concatenate((self.signals[1 * self.Fs:].T, signal.T), axis=1).T

    def plot_audio_signals(self, interval=3, NUM_CHANNELS=1):  # plot the audio signals
        t = np.linspace(0, interval, self.Fs * interval)
        for i in range(NUM_CHANNELS):
            plt.plot(t, self.signals[:, i])
        plt.show()

    @staticmethod
    def end():  # end the raspberry Pi program correctly
        GPIO.cleanup()
