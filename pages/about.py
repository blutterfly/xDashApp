import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/about', name='About')

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Back", href="/")),
    ],
    brand="About",
    color="dark",
    dark=True,
    className="mb-4"
)

layout = dbc.Container([
    navbar,
    html.Hr(),
    html.H2("About Page"),
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Contact", className="card-title"),
                    html.P("Email: yourname@domain.com", className="card-text"),
                    html.P("Phone: 123-456-7890", className="card-text"),
                ]
            )
        ],
        className="mb-3"
    ),
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("About This Application", className="card-title"),
                    html.P(
                        "This Dash multi-page app provides various functionalities: "
                        "portal links, note viewing, stock data, and more."
                    ),
                ]
            )
        ],
        className="mb-3"
    ),
    html.Hr(),
    html.Footer("© 2025 My Company - All Rights Reserved.", style={"textAlign": "center"})
], fluid=True)
