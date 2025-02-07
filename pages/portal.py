import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/portal', name='Portal')

# Load Markdown content from docs/portal.md
portal_markdown = ""
try:
    with open("docs/portal.md", "r", encoding="utf-8") as f:
        portal_markdown = f.read()
except FileNotFoundError:
    portal_markdown = "## Portal Page\n*Placeholder text because `docs/portal.md` not found.*"

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Back", href="/")),
    ],
    brand="Portal",
    color="dark",
    dark=True,
    className="mb-4"
)

# List of external links that open in a new tab
links = [
    {"label": "Google", "href": "https://www.google.com"},
    {"label": "iCloud", "href": "https://www.icloud.com"},
    {"label": "Yahoo",  "href": "https://www.yahoo.com"},
    {"label": "GitHub", "href": "https://www.github.com"},
]

layout = dbc.Container([
    navbar,
    dcc.Markdown(portal_markdown),
    html.Hr(),
    html.Ul([
        html.Li(
            dcc.Link(link["label"], href=link["href"], target="_blank")
        ) for link in links
    ])
], fluid=True)
