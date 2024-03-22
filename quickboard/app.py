import os

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc


def generate_layout(board):
    """
    Creates the layout of the app using a Quickboard object.
    """
    layout = html.Div([
        board,
        dcc.Store(id='data_store', data={'current_tab': "", 'sidebar_controls': []}),
    ])

    return layout

def create_app(board, theme=dbc.themes.BOOTSTRAP, app_title="Dash"):
    app = dash.Dash(__name__, external_stylesheets=[theme], title=app_title)
    app.config.suppress_callback_exceptions = True

    app.layout = generate_layout(board)
    return app


def start_app(board, theme=dbc.themes.BOOTSTRAP, jupyter_mode='external', host=os.getenv("HOST", "127.0.0.1"),
              port=8050, proxy=None, debug=True, app_title="Dash", **flask):
    """
    Takes a Quickboard object and creates app with layout, then runs the app on given port.
    Extra args get sent to Flask server. Theme should be selected from dbc.themes.
    Other nice themes: DARKLY, CYBORG, BOOTSTRAP, FLATLY, LUX, LUMEN, SOLAR.
    """
    app = create_app(board=board, theme=theme, app_title=app_title)
    app.run(host=host, jupyter_mode=jupyter_mode, port=port, proxy=proxy, debug=debug, **flask)


def get_app_server(board, theme=dbc.themes.BOOTSTRAP, app_title="Dash"):
    """
    This method can be used as an alternative to the above for running the app in a production environment, e.g. with
    gunicorn, using the server variable.
    """
    app = create_app(board=board, theme=theme, app_title=app_title)
    return app.server
