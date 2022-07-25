from dash import html
import dash_bootstrap_components as dbc

import quickboard.styles as styles


class Panel:
    """
    An "abstract" class representing a panel holding a single Dash/HTML object.
    Inputs:
        header = header text/object
        main_content = main HTML object to hold
        kwargs = extra keyword arguments become attributes of the object for extending functionality easily
    """
    def __init__(self, header, main_content, **kwargs):
        self.header = html.H3(header, style=styles.PANEL_HEADER_STYLE) if type(header) == str else header
        self.main_content = main_content

        self.container = dbc.Toast([
            self.header, self.main_content
        ],
            style=styles.PANEL_STYLE
        )

        for key, value in kwargs.items():
            setattr(self, key, value)
