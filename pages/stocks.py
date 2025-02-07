import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/stocks', name='Stocks')

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Back", href="/")),
    ],
    brand="Stocks",
    color="dark",
    dark=True,
    className="mb-4"
)

layout = dbc.Container([
    navbar,
    html.H3("Stocks Page"),
    html.P("Execute script 'pages/stocks.py' logic here. Add your stock data, graphs, etc."),
], fluid=True)

# You can add callbacks or other logic below, e.g., retrieving stock data
# from an API or reading from a local CSV.
