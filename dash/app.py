from dash import Dash, html, dcc
import dash

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.Div(
        html.H1("Crypto Tracker",
                style={'margin-top': '50px',
                       'text-transform': 'uppercase',
                       'font-size': '40px',
                       'color': 'black',
                       'text-align': 'center'})
    ),
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),
    dash.page_container
], style={"width": "100%", "overflow": "hidden"})

if __name__ == '__main__':
    app.run_server(debug=True)
