from dash import dcc

from quickboard.primitives import ControlPlugin

class RadioButtons(ControlPlugin):
    """
    Template for creating radio button plugins.
    Inputs:
        data_values = list of possible values to populate the buttons
        header = header text/object
    """
    def __init__(self, data_values, header=""):
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