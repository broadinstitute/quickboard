from dash import dcc

from quickboard.primitives import ControlPlugin


class DataFilterChecklist(ControlPlugin):
    """
    A plugin for filtering data to be displayed by removing records where a certain column's value is not in checklist.
    Inputs:
        header = header text/object
        data_col = column from data to check for values in checklist
        data_values = list of possible values to populate the checklist
    """
    def __init__(self, header, data_col, data_values, **kwargs):
        component = dcc.Checklist
        component_inputs = {
            'options': [
                {'label': x, 'value': x} for x in data_values
            ],
            'value': data_values,
            'labelStyle': {'display': 'block'},
            'inputStyle': {"margin-right": '10px'}
        }

        super().__init__(
            header=header,
            component=component,
            component_inputs=component_inputs,
            **kwargs
        )

        self.control_attributes = {'data_col': data_col}

    # Overrides parent method
    @staticmethod
    def configure(control_attributes, dp, df, control_value):
        """
        Filters the data by checking the column has values in the currently checked values.
        """
        data_col = control_attributes['data_col']
        df = df[df[data_col].isin(control_value)]
        return df, {}
