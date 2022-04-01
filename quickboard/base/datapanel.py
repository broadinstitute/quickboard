from dash import dcc
from dash import dash_table
from dash.dependencies import Input, Output, State, ALL

from quickboard.dashsetup import app
from quickboard.base import DynamicPanel

import pandas as pd


class DataPanel(DynamicPanel):
    """
    A dynamic panel meant to hold a Dash DataTable.
    Inputs:
        html_id = unique name for this component
        header = header text/object
        data_source = key to use in tab data dictionary to get data inputs for this panel
        body = text/objects to present between header and main_content
        plugins = list of plugin objects to load under main_content to use to manipulate main object
        plugin_wrap = number of plugins to load per row underneath main object
        kwargs = extra keyword arguments become attributes of the object for extending functionality easily
    """
    def __init__(self, html_id, header, data_source="data", body="", plugins=[], plugin_wrap=2, **kwargs):
        self.datatable = dash_table.DataTable(
            id=html_id,
            page_action='none',
            sort_action='native',
            filter_action='native',
            fixed_rows={'headers': True},
            style_table={'overflow': 'auto', 'width': '100%', 'height': '275px'}
        )

        super().__init__(
            html_id=html_id,
            header=header,
            main_content=self.datatable,
            data_source=data_source,
            plugins=plugins,
            body=body,
            plugin_wrap=plugin_wrap,
            **kwargs
        )

        # Table update callback
        app.callback(
            Output(self.html_id, 'data'),
            Output(self.html_id, 'columns'),
            Input('data_store', 'data'),
            Input({'type': 'data_control', 'html_id': ALL, 'parent_id': self.html_id}, 'value'),
            State({'type': 'data_control', 'html_id': ALL, 'parent_id': self.html_id}, 'id')
        )(self.update_table)

    def update_table(self, data_state, control_values=[], control_ids=[]):
        """
        A method called to populate the table when the state of a control object is changed.
        """
        df = self.apply_transforms(data_state, control_values, control_ids)

        data = df.to_dict('records')
        columns = [{'id': c, 'name': c} for c in df.columns]
        return (data, columns)
