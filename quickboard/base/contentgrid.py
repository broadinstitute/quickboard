from dash import html

import quickboard.styles as styles

import itertools


class ContentGrid:
    """
    An object for storing other components into a grid.
    Inputs:
        header = header text/object
        content_list = list of objects to store in the grid
        col_wrap = number of objects to display within a row
        content_widths = list of integers between 0 and 100 for percent width for corresponding content_list item
        border = boolean to determine if the grid has a surrounding border
    """
    def __init__(self, header="", content_list=[], col_wrap=2, content_widths=[], border=True):
        self.header = html.H2(header, style=styles.CONTENT_GRID_HEADER_STYLE) if type(header) == str else header

        table_rows = []
        # Break up plot list into equal sized chunks with last row filled with "None" for spillovers
        for i, row in enumerate(itertools.zip_longest(*(iter(content_list),) * col_wrap)):
            table_row = html.Tr([
                html.Td(
                    [x.container],
                    style={
                        "width": f'{content_widths[col_wrap * i + j]}%' if col_wrap * i + j < len(content_widths) else "100%",
                        "padding": "5px"
                    }
                ) for j, x in enumerate(row) if x is not None
            ])
            table_rows.append(table_row)

        self.container = html.Div([
            self.header,
            html.Table(table_rows, style={"width": "100%", 'table-layout': 'fixed'})
        ],
            style=styles.CONTENT_GRID_STYLE if border else styles.CONTENT_GRID_NO_BORDER_STYLE
        )
