import dash
from dash import html, dcc, Output, Input, callback
from utils import get_crypto_graph, datetime_to_millis
import plotly.express as px
from datetime import datetime

dash.register_page(__name__, path="/tracker")

layout = html.Div([
    html.Div([
        html.H2("Options",
                style={'margin-top': '50px',
                       'text-transform': 'uppercase',
                       'font-size': '20px',
                       'color': 'black',
                       'text-align': 'center'}),
        html.P("Pick a crypto and date range to track",
               style={'text-align': 'center',
                      'color': 'black'
                      }),
        html.Img(src="assets/settings.png",
                 style={
                     'width': '320px'
                 }),
        html.Label("Choose a crypto",
                   style={
                       'margin-left': '20px',
                       'color': 'black',
                       'font-weight': 'bold'}),
        dcc.Dropdown(["ethereum", "bitcoin"], id="crypto-dropdown"),
        html.Label("Choose a date range",
                   style={
                       'margin-left': '20px',
                       'color': 'black',
                       'font-weight': 'bold'}),
        html.Div([
            dcc.DatePickerRange(id='date_picker_range'),
        ]),
        html.Button(id='update-button', children="Update",
                    style={'width': '240px', 'height': '40px',
                           'cursor': 'pointer', 'border': '0px',
                           'border-radius': '5px', 'background-color':
                           'black', 'color': 'white', 'text-transform':
                           'uppercase', 'font-size': '15px'})
    ], id='left_container',
        style={'height': '937px',
               'width': '320px',
               'background-color': 'white',
               'float': 'left',
               'margin': '0'},
    ),
    html.Div([
        dcc.Graph(id='crypto_graph',
                  style={"margin-left": "340px"})
    ], id='right-container')
])


@callback(
    Output('crypto_graph', component_property="figure"),
    Input('date_picker_range', 'start_date'),
    Input('date_picker_range', 'end_date'),
    Input('crypto-dropdown', 'value')
)
def update_graph(start_date, end_date, crypto):
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

    start_date_millis = datetime_to_millis(start_date_dt)
    end_date_millis = datetime_to_millis(end_date_dt)

    fig = get_crypto_graph(start_date_millis, end_date_millis, crypto)
    return fig
