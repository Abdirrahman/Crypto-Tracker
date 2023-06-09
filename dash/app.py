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
                        "text-align": "left",
                        "padding": "20px",
                        "margin": "0",
                        "font-family": "Arial, sans-serif",
                        "border": "1px solid #333",
                        "border-radius": "5px",
                    },
                ),
            ],
            style={
                "border": "1px solid #333",
                "border-radius": "5px",
                "padding": "20px",
            },
        ),
        html.Div(
            [
                html.Div(
                    dcc.Link(
                        f"{page['name']}",
                        href=page["relative_path"],
                        style={
                            "margin-right": "10px",
                            "color": "#333",
                            "text-decoration": "none",
                            "font-weight": "bold",
                            "font-size": "18px",
                            "font-family": "Arial, sans-serif",
                            "transition": "background-color 0.3s",
                        },
                    ),
                )
                for page in dash.page_registry.values()
            ],
            style={
                "padding": "10px",
                "text-align": "center",
                "border": "1px solid #333",
                "border-radius": "5px",
            },
            className="navigation",
        ),
        dash.page_container,
    ],
    style={
        "width": "100%",
        "overflow": "hidden",
        "font-family": "Arial, sans-serif",
        "padding": "20px",
        "border": "1px solid #333",
        "border-radius": "5px",
    },
    className="container",
)

if __name__ == "__main__":
    app.run_server(debug=True)
