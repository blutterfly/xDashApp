import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Register this file as a page
dash.register_page(__name__, path='/', name='Home')

# Load Markdown content from docs/home.md
home_markdown = ""
try:
    with open("docs/home.md", "r", encoding="utf-8") as f:
        home_markdown = f.read()
except FileNotFoundError:
    home_markdown = "## Home page\n*Placeholder text because `docs/home.md` not found.*"

# Create a NavBar for demonstration
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Portal", href="/portal")),
        dbc.NavItem(dbc.NavLink("Notes", href="/notes")),
        dbc.NavItem(dbc.NavLink("Blog", href="#")),   # or "/blog" if implemented
        dbc.NavItem(dbc.NavLink("Stocks", href="/stocks")),
        dbc.NavItem(dbc.NavLink("Songs", href="#")),  # placeholder
        dbc.NavItem(dbc.NavLink("Demo", href="#"))    # placeholder
    ],
    brand="My Multi-Page Dash App",
    color="primary",
    dark=True,
    className="mb-4"
)

layout = dbc.Container([
    navbar,
    # Render the Markdown describing the functions and contents of each page
    dcc.Markdown(home_markdown)
], fluid=True)
