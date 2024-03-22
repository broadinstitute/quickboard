from dash import dcc
import dash_bootstrap_components as dbc

from quickboard.primitives import ControlPlugin

class Dropdown(ControlPlugin):
    """
    Template for creating dropdown plugins.
    Inputs:
        data_values = list of possible values to populate the menu
        header = header text/object
    """
    def __init__(self, data_values, header=""):
        component = dcc.Dropdown
        component_inputs = {
            'options': [
                {'label': x, 'value': x} for x in data_values
            ],
            'value': data_values[0],
            # 'labelStyle': {'display': 'block'},
            # 'inputStyle': {'margin-right': '10px'}
        }

        super().__init__(
            header=header,
            component=component,
            component_inputs=component_inputs
        )

        self.style = self.style | {'margin-right': '10px'}