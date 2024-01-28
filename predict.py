import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# from tensorflow.keras.models import load_model
# loaded_model = load_model('my_model.h5')

def predict(model, df):

    def create_feature(df):
        # create features from the selected machine
        pressure = df['pressure']
        timestamp = pd.to_datetime(df['datetime'])
        timestamp_hour = timestamp.map(lambda x: x.hour)
        timestamp_hour_onehot = pd.get_dummies(timestamp_hour).to_numpy()

        scaler = MinMaxScaler()
        pressure = scaler.fit_transform(np.array(pressure).reshape(-1,1))
        feature = np.concatenate([pressure, timestamp_hour_onehot], axis=1)

        X = feature[:-1]
        y = np.array(feature[5:,0]).reshape(-1,1)

        return X, y, scaler

    def shape_sequence(arr, step, start):
        out = list()
        for i in range(start, arr.shape[0]):
            low_lim = i
            up_lim = low_lim + step
            out.append(arr[low_lim: up_lim])

            if up_lim == arr.shape[0]:
                break

        out_seq = np.array(out)
        return out_seq

    X_test, _, _ = create_feature(df)

    # Shape the sequence 
    X_test_seq = shape_sequence(X_test, 5, 0)

    # Predict the testing data
    return model.predict(X_test_seq)



# def plot(model, df, start, end):
#     def create_feature(df, start, end):
#         # create features from the selected machine
#         pressure = df.loc[start: end, 'pressure']
#         timestamp = pd.to_datetime(df.loc[start: end, 'datetime'])
#         timestamp_hour = timestamp.map(lambda x: x.hour)

#         # apply one-hot encode for timestamp data
#         timestamp_hour_onehot = pd.get_dummies(timestamp_hour).to_numpy()

#         # apply min-max scaler to numerical data
#         scaler = MinMaxScaler()
#         pressure = scaler.fit_transform(np.array(pressure).reshape(-1,1))

#         # combine features into one
#         feature = np.concatenate([pressure, timestamp_hour_onehot], axis=1)

#         X = feature[:-1]
#         y = np.array(feature[5:,0]).reshape(-1,1)

#         return X, y, scaler

#     def shape_sequence(arr, step, start):
#         out = list()
#         for i in range(start, arr.shape[0]):
#             low_lim = i
#             up_lim = low_lim + step
#             out.append(arr[low_lim: up_lim])

#             if up_lim == arr.shape[0]:
#                 break

#         out_seq = np.array(out)
#         return out_seq


#     X_test, y_test, test_scaler = create_feature(df, start, end)

#     # Shape the sequence 
#     X_test_seq = shape_sequence(X_test, 5, 0)
#     y_test_seq = shape_sequence(y_test, 1, 0)

#     # Predict the testing data
#     y_pred_test = model.predict(X_test_seq)

#     # Select first 200 datapoints to allow for better plotting
#     # Return the value using inverse transform to allow better observation
#     fig = plt.figure
#     plt.plot(test_scaler.inverse_transform(y_pred_test[:200].reshape(-1, 1)), 'r', label='Prediction')
#     plt.plot(test_scaler.inverse_transform(y_test_seq[:200].reshape(-1, 1)), 'k', label='Original')
#     plt.ylabel("Pressure")
#     plt.xlabel("Datapoints")
#     # plt.axvline(x=7*24, color='g', linestyle='--', label='Today')
#     plt.legend()
#     return fig

    
def failure(model, df):
    """
    Predicts pressures of the machine from the given time range

    Parameters
    ----------
    model : tensorflow.keras.models.Model
        The model used for prediction
    df : pandas.DataFrame
        The dataframe containing columns of datetime and pressure
        
    Returns
    -------
    numpy.ndarray
        The predicted pressures of the machine
    """

    predictions = predict(model, df)

    past = predictions[:-24]
    present = predictions[-24:] # last 24 hours

    past_std = np.std(past)
    past_average = np.mean(past)

    present_average = np.mean(present)

    if present_average > past_average + 2 * past_std:
        return True
    else:
        return False


