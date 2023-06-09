from dash import Dash, html, dcc
import dash

app = Dash(__name__, use_pages=True)

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "Crypto Tracker",
                    style={
                        "text-transform": "uppercase",
                        "font-size": "40px",
                        "color": "#333",
                        "text-align": "center",
                        "padding": "20px",
                        "margin": "0",
                        "font-family": "Arial, sans-serif",
                    },
                ),
            ],
        ),
        html.Div(
            [
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}",
                        href=page["relative_path"],
                        style={
                            "margin-right": "10px",
                            "color": "#333",
                            "text-decoration": "none",
                            "font-weight": "bold",
                            "font-size": "18px",
                            "font-family": "Arial, sans-serif",
                        },
                    ),
                )
                for page in dash.page_registry.values()
            ],
            style={"padding": "10px", "text-align": "center"},
        ),
        dash.page_container,
    ],
    style={"width": "100%", "overflow": "hidden",
           "font-family": "Arial, sans-serif"},
)


if __name__ == '__main__':
    app.run_server(debug=True)
