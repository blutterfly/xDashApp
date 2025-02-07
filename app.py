# app.py
import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

# Initialize the Dash app
# Note: Dash pages auto-discovery is on by default (Dash 2.5+).
#       You must have 'pages' in your PYTHONPATH or within the same directory.
app = Dash(
    __name__,
    use_pages=True,  # Enables Dash multi-page feature
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server  # Expose the server if you need to deploy on platforms like Heroku

# Define a top-level layout that simply contains Dash's Page Container
app.layout = dbc.Container([
    dash.page_container  # This will render the layout of the current page
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
