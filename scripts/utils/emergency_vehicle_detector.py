# import packages
import tensorflow as tf
import numpy as np
from sklearn.metrics import confusion_matrix


class EmergencyVehicle:
    def __init__(self, model_path, weights_path):
        # load the trained neural network model
        self.MODEL = tf.keras.models.load_model(model_path)
        self.MODEL.load_weights(weights_path)
        self.threshold = 0.5

    def detector(self, spectrogram):  # detect the presence of siren
        spectrogram = np.reshape(spectrogram, (1, spectrogram.shape[0], spectrogram.shape[1], 1))
        pred = self.MODEL.predict(spectrogram)[0][0]
        if pred >= self.threshold:
            return True
        return False

    def emergency_vehicle_detection(self, spectrograms):  # detect the presence of siren for all the microphones
        return tuple(map(self.detector, spectrograms))

    @staticmethod
    def show_results(y_true, y_pred):  # get results of the model
        print(confusion_matrix(y_true, y_pred))
