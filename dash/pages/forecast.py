import dash
import numpy as np
import pandas as pd
from dash import html, dcc, Output, Input, callback
import plotly.express as px
from sklearn.svm import SVR

from forecast_model import load_prediction_data, load_training_data, dataframe_data, clean_data, independent_dataset, dependent_dataset, split_dataset
from utils import get_crypto_list

dash.register_page(__name__, path="/forecast")


layout = html.Div(
    [
        html.Div(
            [
                html.H2(
                    "Options",
                    style={
                        "margin-top": "50px",
                        "text-transform": "uppercase",
                        "font-size": "20px",
                        "color": "black",
                        "text-align": "center",
                    },
                ),
                html.P(
                    "Pick a cryptocurrency and date range to track",
                    style={"text-align": "center", "color": "black"},
                ),
                html.Img(src="assets/settings.png", style={"width": "320px"}),
                html.Label(
                    "Choose a cryptocurrency",
                    style={
                        "margin-top": "20px",
                        "margin-bottom": "10px",
                        "color": "black",
                        "font-weight": "bold",
                    },
                ),
                dcc.Dropdown(
                    options=get_crypto_list(),
                    id="crypto-dropdown",
                ),

                html.Button(
                    id="update-button",
                    children="Update",
                    style={
                        "width": "240px",
                        "height": "40px",
                        "cursor": "pointer",
                        "border": "0px",
                        "border-radius": "5px",
                        "background-color": "black",
                        "color": "white",
                        "text-transform": "uppercase",
                        "font-size": "15px",
                        "margin-top": "20px",
                    },
                ),
            ],
            id="left-container",
            style={
                "height": "937px",
                "width": "320px",
                "background-color": "white",
                "float": "left",
                "padding": "20px",
            },
        ),
        html.Div(
            [
                dcc.Graph(
                    id="forecast_graph",
                    figure={"layout": {"title": "Chosen Graph"}},
                    style={"margin-left": "20px"},
                ),

            ],
            id="right-container",
            style={"padding": "20px", "margin-left": "360px"},
        ),
    ]
)


@callback(
    Output('forecast_graph', 'figure'),
    Input('update-button', 'n_clicks'),
    Input('crypto-dropdown', 'value')
)
def update_graph(n_clicks, crypto):
    if n_clicks is None:
        # No button click yet, return initial figures
        return {"layout": {"title": "Chosen Cryptocurrency Graph"}}

    #  Plot graph to forecast data currently set to the next 30 days.
    prediction_data = load_prediction_data(crypto)
    training_data = load_training_data(crypto)

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

    return fig
