import os

from dash import html
from dash import dcc

from quickboard.dashsetup import app
from quickboard.utils.environment import isnotebook


def start_app(board, mode='external', host=os.getenv("HOST", "127.0.0.1"), port=8050):
    """
    Takes an app instance and configures its board layout, then runs the app on given port.
    """
    app.layout = html.Div([
        board.container,
        dcc.Store(id='data_store', data={'callback_num': 0}),
    ])

    if isnotebook():
        app.run_server(mode=mode, debug=True, host=host, port=port)
    else:
        app.run_server(debug=True, host=host, port=port)
