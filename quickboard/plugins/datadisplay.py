from dash import html, callback
from dash import dash_table
from dash.dependencies import Input, Output

import pandas as pd
from quickboard.primitives import Panel


class DataDisplay(Panel):
    """
    A plugin for showing data beneath a DynamicPanel, with listening capabilities.
    Inputs:
        data_source = key to use in tab data dictionary to get data inputs for this panel
        header = header text/object
        listen = list of control objects to get notified of changes in them
    """
    def __init__(self, data_source, header="", listen=[]):
        # Calibrate header based on input and control type
        if isinstance(header, str):
            self.header = html.H5(header)
        else:
            self.header = header

        self.data_source = data_source

        self.datatable = dash_table.DataTable(
            page_action='none',
            sort_action='native',
            filter_action='native',
            fixed_rows={'headers': True},
            style_table={'height': '150px', 'overflow': 'auto', 'overflowX': 'scroll', 'width': '100%'}
        )

        super().__init__(main_content=[self.header, self.datatable])

        callback(
            Output(self.datatable, 'data'),
            Output(self.datatable, 'columns'),
            Input('data_store', 'data'),
            [Input(x, 'value') for x in listen]
        )(self.update_table)

    def data_transform(self, df):
        """
        A method for transforming the data before getting put into the table.
        """
        return df

    def update_table(self, data_state, *inputs):
        """
        Callback method for manipulating the data before getting put into the table. Use the `inputs` list to get
        the new states of the control objects declared in the __init__ `listen` list. Must return a tuple
        `(data, columns)` where `data` is a dict of records (e.g. df.to_dict('records')) and columns is a list of
        dictionaries with keys 'id' and 'name' (e.g. [{'id': c, 'name': c} for c in df.columns]).
        """
        df = pd.DataFrame.from_dict(data_state[self.data_source])
        df = self.data_transform(df)

        data = df.to_dict('records')
        columns = [{'id': c, 'name': c} for c in df.columns]
        return (data, columns)