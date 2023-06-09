import dash
from dash import html, dcc, Output, Input, callback
from utils import get_crypto_graph, datetime_to_millis, get_crypto_list
import plotly.express as px
from datetime import datetime

dash.register_page(__name__, path="/tracker")

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
                        "border": "1px solid #333",
                        "border-radius": "5px",
                    },
                ),
                html.P(
                    "Pick a cryptocurrency and date range to track",
                    style={"text-align": "center", "color": "black"},
                ),
                html.Img(
                    src="assets/settings.png",
                    style={"width": "320px"},
                ),
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
                html.Label(
                    "Choose a date range",
                    style={
                        "margin-top": "20px",
                        "margin-bottom": "10px",
                        "color": "black",
                        "font-weight": "bold",
                    },
                ),
                dcc.DatePickerRange(id="date_picker_range"),
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
                "border": "1px solid #333",
                "border-radius": "5px",
            },
        ),
        html.Div(
            [
                dcc.Graph(
                    id="bitcoin_graph",
                    figure={"layout": {"title": "Bitcoin Graph"}},
                    style={"margin-left": "20px"},
                ),
                dcc.Graph(
                    id="crypto_graph",
                    figure={"layout": {"title": "Chosen Cryptocurrency Graph"}},
                    style={"margin-left": "20px"},
                ),
            ],
            id="right-container",
            style={
                "padding": "20px",
                "margin-left": "360px",
                "border": "1px solid #333",
                "border-radius": "5px",
            },
        ),
    ],
    className="container",
)


@callback(
    Output('crypto_graph', 'figure'),
    Output('bitcoin_graph', 'figure'),
    Input('update-button', 'n_clicks'),
    Input('date_picker_range', 'start_date'),
    Input('date_picker_range', 'end_date'),
    Input('crypto-dropdown', 'value')
)
def update_graph(n_clicks, start_date, end_date, crypto):
    if n_clicks is None:
        # No button click yet, return initial figures
        return {"layout": {"title": "Chosen Cryptocurrency Graph"}}, {"layout": {"title": "Bitcoin Graph"}}

    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

    start_date_millis = datetime_to_millis(start_date_dt)
    end_date_millis = datetime_to_millis(end_date_dt)

    fig = get_crypto_graph(start_date_millis, end_date_millis, crypto)
    fig_btc = get_crypto_graph(start_date_millis, end_date_millis, 'bitcoin')
    return fig, fig_btc
