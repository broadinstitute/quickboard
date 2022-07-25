from dash import dcc

from quickboard.primitives import ControlPlugin


class DataFilterRadioButtons(ControlPlugin):
    """
    A plugin for filtering data to be displayed by removing records where a certain column's value does not equal the
    selected radio button value.
    Inputs:
        header = header text/object
        data_col = column from data to check for values matching button
        data_values = list of possible values to populate the radio button list
    """
    def __init__(self, header, data_col, data_values):
        component = dcc.RadioItems
        component_inputs = {
            'options': [
                {'label': x, 'value': x} for x in data_values
            ],
            'value': data_values[0],
            'labelStyle': {'display': 'block'},
            'inputStyle': {"margin-right": '10px'}
        }

        super().__init__(
            header=header,
            component=component,
            component_inputs=component_inputs
        )

        self.control_attributes = {'data_col': data_col}

    # Overrides parent method
    @staticmethod
    def configure(control_attributes, dp, df, control_value):
        """
        Filters the data by checking the column has value matching the selected button.
        """
        data_col = control_attributes['data_col']
        df = df[df[data_col] == control_value]
        return df, {}
