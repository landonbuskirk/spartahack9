from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow.keras.losses as loss
import os
import pandas as pd

class ForcastingModel:

    def __init__(self, input_shape, output_shape, learning_rate=0.001, loss=MeanSquaredError()):
        self.model = Sequential()
        self.model.add(LSTM(input_shape[1], activation='tanh', input_shape=input_shape, return_sequences=True))
        self.model.add(LSTM(input_shape[1], activation='tanh', input_shape=input_shape, return_sequences=False))
        self.model.add(Dense(input_shape[1], activation='relu'))
        self.model.add(Dense(1, activation='linear'))
        self.model.add(Dense(output_shape))
        self.model.compile(optimizer=Adam(learning_rate), loss=loss)
        self.model.summary()

    def train(self, X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, save_path=None):
        if save_path is None:
            save_path = os.path.join(os.getcwd(), 'models')
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        checkpoint_path = os.path.join(save_path, 'model-{epoch:02d}-{val_loss:.2f}.hdf5')
        checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=validation_split, callbacks=[checkpoint])

    def predict(self, X_test):
        return self.model.predict(X_test)

    def load_model(self, path):
        self.model.load_weights(path)

    def save_model(self, path):
        self.model.save_weights(path)

    def evaluate(self, X_test, y_test):
        return self.model.evaluate(X_test, y_test)

    def get_model(self):
        return self.model

    def get_weights(self):
        return self.model.get_weights()

    def set_weights(self, weights):
        self.model.set_weights(weights)

    def get_layer_output(self, X_test, layer_index):
        return self.model.layers[layer_index].output

    def get_layer_weights(self, layer_index):
        return self.model.layers[layer_index].get_weights()

    def set_layer_weights(self, layer_index, weights):
        self.model.layers[layer_index].set_weights(weights)

    def get_layer(self, layer_index):
        return self.model.layers[layer_index]

    def get_layer_output_shape(self, layer_index):
        return self.model.layers[layer_index].output_shape