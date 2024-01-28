import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow.keras.losses as loss

WORKING_DIR = os.getcwd()

df_tele = pd.read_csv(WORKING_DIR + '/data/PdM_telemetry.csv')
df_fail = pd.read_csv(WORKING_DIR + '/data/PdM_failures.csv')
df_err = pd.read_csv(WORKING_DIR + '/data/PdM_errors.csv')
df_maint = pd.read_csv(WORKING_DIR + '/data/PdM_maint.csv')

df_sel = df_tele.loc[df_tele['machineID'] == 11].reset_index(drop=True)

st_train = df_sel.loc[df_sel['datetime'] == pd.to_datetime("2015-02-19")].index.values[0]

st_train = df_sel.loc[df_sel['datetime'] == pd.to_datetime("2015-02-19")].index.values[0]
start_period = st_train - 14*24
end_period = st_train + 14*24

def shape_sequence(arr, step, start):
    out = list()
    for i in range(start, arr.shape[0]):
        low_lim = i
        up_lim = low_lim + step
        out.append(arr[low_lim: up_lim])

        if up_lim == arr.shape[0]:
          # print(i)
          break

    out_seq = np.array(out)
    return out_seq

X_seq = shape_sequence(X, 5, 0)
y_seq = shape_sequence(y, 1, 0)

X_train, X_val, y_train, y_val = train_test_split(X_seq, y_seq, test_size=0.2, shuffle=False)


def create_model(X_train, y_train):
  shape = X_train.shape[1]
  feat_length = X_train.shape[2]

  model = Sequential()
  model.add(LSTM(shape, activation='tanh', input_shape=(shape, feat_length), return_sequences=True))
  model.add(LSTM(shape, activation='tanh', input_shape=(shape, feat_length), return_sequences=False))
  model.add(Dense(shape, activation='relu'))
  model.add(Dense(1, activation='linear'))
  model.compile(optimizer=Adam(lr=0.035),
                loss=loss.mean_squared_error)
  model.fit(X_train, y_train, verbose=1, epochs=500)

  return model

model = create_model(X_train, y_train)

y_pred = model.predict(X_val)
mse = MeanSquaredError()
val_err = mse(y_val.reshape(-1,1), y_pred)
print("Validation error = ", val_err.numpy())

model.save('my_model.h5')