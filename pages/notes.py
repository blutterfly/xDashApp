import os
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash import dash_table
import csv
import urllib.parse as urlparse
from urllib.parse import parse_qs

dash.register_page(__name__, path="/notes", name="Notes", title="Notes Page")

# A simple NavBar example
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Back", href="/")),  # or another page if desired
    ],
    brand="Notes",
    color="dark",
    dark=True,
    className="mb-4"
)

def layout():
    """
    Layout function that returns a container with:
      1. Navbar
      2. A dcc.Location to listen for URL changes (query params)
      3. A file listing
      4. A content area
    """
    # List all files in 'notes/' (non-recursive, simplest approach)
    files = [f for f in os.listdir("notes") 
             if os.path.isfile(os.path.join("notes", f))]

    # Create a list of HTML <li> items, each linking to ?file=<FILENAME>
    file_links = [
        html.Li(
            html.A(
                file_name,
                href=f"/notes?file={file_name}",  # query param
                style={"textDecoration": "none"}
            )
        )
        for file_name in sorted(files)
    ]

    return dbc.Container([
        navbar,
        dcc.Location(id="notes-url", refresh=False),
        html.H4("Files in 'notes' folder:"),
        html.Ul(file_links),
        html.Hr(),
        html.Div(id="notes-content", children="Select a file to display its content."),
    ], fluid=True)

@dash.callback(
    Output("notes-content", "children"),
    [Input("notes-url", "search")]
)
def display_file_content(search):
    """
    Callback that listens to the URL's query string (?file=FILENAME).
    If present, reads that file from the 'notes/' folder and displays content
    based on extension (.md, .txt, .csv).
    """
    if not search:
        # No query string => just show a default message
        return "Select a file to display its content."

    # Parse query string, e.g. ?file=example.md
    parsed = urlparse.urlparse(search)
    params = parse_qs(parsed.query)
    filename = params.get("file", [None])[0]  # extract 'file' param

    if not filename:
        return "Select a file to display its content."

    # Construct the path in the notes folder
    full_path = os.path.join("notes", filename)
    if not os.path.exists(full_path):
        return f"Error: file '{filename}' not found in the notes folder."

    # Determine extension for proper rendering
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    try:
        if ext == ".md":
            # Render as Markdown
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            return dcc.Markdown(content, link_target="_blank")

        elif ext == ".csv":
            # Render as Dash DataTable
            rows = []
            with open(full_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)

            if not rows:
                return "This CSV file is empty."

            header = rows[0]
            data = rows[1:]
            return dash_table.DataTable(
                columns=[{"name": col, "id": str(i)} for i, col in enumerate(header)],
                data=[{str(i): cell for i, cell in enumerate(row)} for row in data],
                page_size=10,
                style_table={"overflowX": "auto"}
            )

        else:
            # Assume plain text
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            return html.Pre(content, style={"whiteSpace": "pre-wrap"})
    except Exception as e:
        return html.Div([
            html.P(f"An error occurred while reading '{filename}':"),
            html.Code(str(e), style={"color": "red"})
        ])
