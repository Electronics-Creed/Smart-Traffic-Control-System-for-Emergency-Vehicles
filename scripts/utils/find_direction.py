# import packages
import numpy as np
import scipy.signal as sps


class Direction:
    def __init__(self):
        self.SPEED_OF_SOUND = 331  # speed of sound in m/s
        self.dist = 0.1  # distance between mic and the origin in m
        self.Fs = 22050  # sampling frequency
        self.x = (0.06, 0.16)  # value of x for calculation of slope

    def y_position(self, x, AB):  # given the position in x-axis it gives the possible position in y-axis
        return np.sqrt((AB ** 2) / 4 - (self.dist ** 2) + (x ** 2) * (4 * (self.dist ** 2) / (AB ** 2) - 1))

    def calculate_delay(self, sig1, sig2):  # calculate the time delay between the two signals
        similarity = sps.correlate(sig1, sig2, mode="full")  # calculating the auto-correlation between the signals
        lag = sps.correlation_lags(len(sig1), len(sig2), mode="full")
        I = np.argmax(np.abs(similarity))  # finding the index of max similarity
        return lag[I] / self.Fs

    def calculate_angle(self, sigs):  # calculate the direction of emergency vehicle
        delay = self.calculate_delay(sigs[0], sigs[1])  # get the delay between the signals
        AB = delay * self.SPEED_OF_SOUND
        slope = (self.y_position(self.x[1], AB) - self.y_position(self.x[0], AB)) / (self.x[1] - self.x[0])  # calculating the slope
        return np.arctan(slope)
