from datetime import datetime
import dash
import numpy as np
import pandas as pd
from dash import html, dcc
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR

from forecast_model import load_prediction_data, load_training_data, dataframe_data, clean_data, independent_dataset, dependent_dataset, split_dataset


dash.register_page(__name__, path="/forecast")

#  Plot graph to forecast data currently set to the next 30 days.
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

prediction_dataframe['date'] = pd.to_datetime(prediction_dataframe['date'])
prediction_dataframe['date'] = prediction_dataframe['date'] + \
    pd.Timedelta(days=30)

fig = px.line(x=prediction_dataframe['date'], y=predicted_forecast)

layout = html.Div(
    [dcc.Graph(id="plot", figure=fig)]
)
