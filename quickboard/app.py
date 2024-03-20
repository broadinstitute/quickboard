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
        board.container,
        dcc.Store(id='data_store', data={'current_tab': "", 'sidebar_controls': []}),
    ])

    return layout


def start_app(board, theme=dbc.themes.BOOTSTRAP, jupyter_mode='external', host=os.getenv("HOST", "127.0.0.1"),
              port=8050, proxy=None, debug=True, app_title="Dash", **flask):
    """
    Takes an app instance and configures its board layout, then runs the app on given port. Extra args get sent to Flask server.
    Theme should be selected from dbc.themes.
    Other nice themes: DARKLY, CYBORG, BOOTSTRAP, FLATLY, LUX, LUMEN, SOLAR.
    """

    app = dash.Dash(__name__, external_stylesheets=[theme], title=app_title)
    app.config.suppress_callback_exceptions = True

    app.layout = generate_layout(board)

    app.run(host=host, jupyter_mode=jupyter_mode, port=port, proxy=proxy, debug=debug, **flask)


# def deploy_app(board):
#     """
#     This method can be used as an alternative to the above for running the app in a production environment, e.g. with
#     gunicorn, using the server variable.
#     """
#     app.layout = generate_layout(board)
#
#     global server
#     server = app.server
