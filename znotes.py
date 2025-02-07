import os
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dash import dash_table
import json
dash.register_page(__name__, path='/notes', name='Notes')

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Back", href="/")),
    ],
    brand="Notes",
    color="dark",
    dark=True,
    className="mb-4"
)

# Function to collect all files from a directory (and subdirs) - optional recursion
def list_notes_files(root_dir="notes"):
    file_list = []
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            # Only gather certain file types or gather all
            if f.lower().endswith(('.md', '.csv', '.txt')):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, root_dir)
                file_list.append(rel_path)
    print(file_list)            
    return sorted(file_list)

layout = dbc.Container([
    navbar,
    dbc.Row([
        dbc.Col(
            [
                html.H4("Available Notes"),
                html.Div(
                    id="notes-list",
                    children=[
                        # We will create a simple list of links or buttons for each file
                        dbc.Button(
                            file,
                            id={'type': 'notes-button', 'index': file},
                            color="secondary",
                            className="m-1",
                            n_clicks=0
                        )
                        for file in list_notes_files()
                    ]
                )
            ],
            width=3
        ),
        dbc.Col(
            [
                html.H4("File Content"),
                html.Div(id='notes-content', children="Select a file to see content.")
            ],
            width=9
        )
    ])
], fluid=True)


@dash.callback(
    Output('notes-content', 'children'),
    [Input({'type': 'notes-button', 'index': dash.ALL}, 'n_clicks')],
    [State({'type': 'notes-button', 'index': dash.ALL}, 'id')]
)
def display_file_content(n_clicks_list, button_ids):
    """
    Triggered when any of the file buttons is clicked.
    We find which button triggered the callback, then read & display that file.
    """
    if not n_clicks_list or not button_ids:
        return "Select a file to see content."

    # Determine which button triggered the callback by checking which n_clicks changed
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Select a file to see content."
    

    trigger_prop_id = ctx.triggered[0]["prop_id"]
    # trigger_prop_id might be something like:
    #   '{"type":"notes-button","index":"sample.md"}.n_clicks'
    # or possibly "notes-list.n_clicks" in some cases

    # Split off the property name (e.g. ".n_clicks").
    # The first part should be the JSON string if it’s a button click.
    trigger_id_str, _ = trigger_prop_id.split(".", 1)

    # If the string doesn't start with '{', it's not JSON => skip
    
    if not trigger_id_str.startswith("{"):
        return "Select a file to see content."

    try:
        trigger_id_dict = json.loads(trigger_id_str)
    except json.JSONDecodeError:
        return "Select a file to see content."




    
    selected_file = trigger_id_dict['index']  # e.g. "sample.md"
    if not selected_file:
        return "No file selected."
    
    full_path = os.path.join("notes", selected_file)
    if not os.path.exists(full_path):
        return f"Error: File {selected_file} not found."

    ext = os.path.splitext(selected_file)[1].lower()

    try:
        if ext == ".md":
            # Render as Markdown
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return dcc.Markdown(content)

        elif ext == ".csv":
            # Parse as CSV and display as dash_table
            import csv
            rows = []
            with open(full_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    rows.append(row)
            if not rows:
                return "Empty CSV file."
            header = rows[0]
            data = rows[1:]
            return dash_table.DataTable(
                columns=[{"name": col, "id": str(i)} for i, col in enumerate(header)],
                data=[
                    {str(i): cell for i, cell in enumerate(row)}
                    for row in data
                ],
                page_size=10
            )

        else:  # treat as plain text
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Show in a <pre> tag or as a scrollable div
            return html.Pre(content)

    except Exception as e:
        return f"An error occurred reading {selected_file}: {e}"
