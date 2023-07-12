import os
from datetime import datetime
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, RNN, Dense, Activation, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from ingestion import get_prediction_data, get_training_data
from eth import get_crypto_data
import plotly.express as px


# Set Forecast
FUTURE_DAYS = 30


def load_prediction_data() -> dict:
    '''Returns ETH prediction data as JSON'''
    load_dotenv()
    eth_prediction = get_prediction_data(auth_token=os.environ['api_key'])
    prediction_data = eth_prediction['data']

    return prediction_data


def load_training_data() -> dict:
    '''Returns ETH training data'''
    eth_train = get_training_data(auth_token=os.environ['api_key'])
    train_data = eth_train['data']

    return train_data


def dataframe_data(data: dict):
    '''Puts data into a dataframe'''

    dataframe = pd.DataFrame(data)

    return dataframe

# prediction_dataframe = pd.DataFrame(prediction_data)


def clean_data(dataframe):
    '''Cleans dataframe'''

    dataframe['date'] = pd.to_datetime(dataframe['date'])
    dataframe['date'] = dataframe['date'].dt.strftime("%Y-%m-%d")

    dataframe['priceUsd'] = dataframe['priceUsd'].astype(float)
    dataframe['priceUsd'] = dataframe['priceUsd'].round(2)

    dataframe[str(
        FUTURE_DAYS)+'_Day_Price_Forecast'] = dataframe[['priceUsd']].shift(-FUTURE_DAYS)

    dataframe = dataframe.set_index(pd.DatetimeIndex(dataframe['date'].values))

    return dataframe


def independent_dataset(dataframe) -> list:
    '''Independent training dataset'''
    X = np.array(dataframe[['priceUsd']])
    X = X[:dataframe.shape[0] - FUTURE_DAYS]

    return X


def dependent_dataset(dataframe) -> list:
    '''Dependent training dataset'''
    y = np.array(dataframe[str(FUTURE_DAYS)+'_Day_Price_Forecast'])
    y = y[:-FUTURE_DAYS]

    return y


def split_dataset(X, y):
    # Split the data
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    return x_train, x_test, y_train, y_test


if __name__ == '__main__':

    prediction_data = load_prediction_data()
    training_data = load_training_data()

    prediction_dataframe = dataframe_data(prediction_data)
    training_dataframe = dataframe_data(training_data)

    prediction_dataframe = clean_data(prediction_dataframe)
    training_dataframe = clean_data(training_dataframe)

    X = independent_dataset(training_dataframe)
    y = dependent_dataset(training_dataframe)

    x_train, x_test, y_train, y_test = split_dataset(X, y)

    # Train SVR model
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.00001)
    svr_rbf.fit(x_train, y_train)

    X_pred = np.array(prediction_dataframe[['priceUsd']])
    predicted_forecast = svr_rbf.predict(X_pred)

    px.line(x=prediction_dataframe['date'], y=predicted_forecast)
