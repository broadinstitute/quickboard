import os

from dash import html
from dash import dcc

from quickboard.dashsetup import app
from quickboard.utils.environment import isnotebook


def generate_layout(board):
    """
    Creates the layout of the app using a Quickboard object.
    """
    layout = html.Div([
        board.container,
        dcc.Store(id='data_store', data={'current_tab': "", 'sidebar_controls': []}),
    ])

    return layout


def start_app(board, mode='external', host=os.getenv("HOST", "127.0.0.1"), port=8050, proxy=None, debug=True, **flask):
    """
    Takes an app instance and configures its board layout, then runs the app on given port. Extra args get sent to
    Flask server.
    """
    app.layout = generate_layout(board)

    if isnotebook():
        app.run_server(mode=mode, host=host, port=port, proxy=proxy, debug=debug, **flask)
    else:
        app.run(host=host, port=port, proxy=proxy, debug=debug, **flask)


def deploy_app(board):
    """
    This method can be used as an alternative to the above for running the app in a production environment, e.g. with
    gunicorn, using the server variable.
    """
    app.layout = generate_layout(board)

    global server
    server = app.server
