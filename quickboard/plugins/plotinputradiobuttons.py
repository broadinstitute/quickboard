from dash import dcc

from quickboard.primitives import ControlPlugin


class PlotInputRadioButtons(ControlPlugin):
    """
    A plugin for modifying a PlotPanel's plotting behavior. The `plot_input` value can be dynamically changed based on
    the selection via radio buttons.
    Inputs:
        header = header text/object
        plot_input = name of the PlotPanel's plotter input to be changed by clicking the radio buttons
        data_values = list of possible values to populate the radio button list
    """
    def __init__(self, header, plot_input, data_values):
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

        self.control_attributes = {'plot_input': plot_input}

    # Overrides parent method
    @staticmethod
    def configure(control_attributes, dp, df, control_value):
        """
        Updates a PlotPanel's plot_inputs attribute to have new value equal to that selected by buttons.
        """
        plot_input = control_attributes['plot_input']
        update = {plot_input: control_value}
        return df, {'plot_inputs': update}
