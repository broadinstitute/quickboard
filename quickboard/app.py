import os

from dash import html
from dash import dcc

from quickboard.dashsetup import app
from quickboard.utils.environment import isnotebook


def start_app(board, host=os.getenv("HOST", "127.0.0.1"), port=8050, extra_stores=[]):
    """
    Takes an app instance and configures its board layout, then runs the app on given port. Use extra_stores for
    extra data stores.
    """
    app.layout = html.Div([
        board.container,
        dcc.Store(id='sidebar_state', data={}),
        dcc.Store(id='data_store', data={}),
    ] + [
        dcc.Store(id=name, data={}) for name in extra_stores
    ])

#    if __name__ == '__main__':
#        app.run_server(debug=True, port=port)
    if isnotebook():
        app.run_server(mode='external', debug=True, host=host, port=port)
    else:
        app.run_server(debug=True, host=host, port=port)
#    else:
#        print("ERROR: Improper environment for running Dash app.")
