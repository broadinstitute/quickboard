from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import quickboard.styles as styles

import itertools


class ContentGrid:
    """
    An object for storing other components into a grid.
    Inputs:
        header = header text/object
        content_list = list of objects to store in the grid
        col_wrap = number of objects to display within a row
        border = boolean to determine if the grid has a surrounding border
    """
    def __init__(self, header="", content_list=[], col_wrap=2, border=True):
        self.header = html.H2(header, style=styles.CONTENT_GRID_HEADER_STYLE) if type(header) == str else header

        table_rows = []
        table_entry_width = f'{round(100 / col_wrap, 2)}%'
        # Break up plot list into equal sized chunks with last row filled with "None" for spillovers
        for row in itertools.zip_longest(*(iter(content_list),) * col_wrap):
            table_row = html.Tr([
                html.Td(
                    [x.container],
                    style={"width": "100%", "padding": "5px"}
                ) for x in row if x is not None
            ])
            table_rows.append(table_row)

        self.container = html.Div([
            self.header,
            html.Table(table_rows, style={"width": "100%", 'table-layout': 'fixed'})
        ],
            style=styles.CONTENT_GRID_STYLE if border else styles.CONTENT_GRID_NO_BORDER_STYLE
        )
