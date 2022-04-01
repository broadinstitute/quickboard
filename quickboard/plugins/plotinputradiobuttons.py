from dash import dcc

from quickboard.base import ControlPlugin


class PlotInputRadioButtons(ControlPlugin):
    """
    A plugin for modifying a PlotPanel's plotting behavior. The `plot_input` value can be dynamically changed based on
    the selection via radio buttons.
    Inputs:
        html_id = unique name for this component
        parent_id = html_id of the parent object holding this plugin
        header = header text/object
        control_type = must be either 'plot_control', 'data_control', or 'sidebar_control' depending on where it appears
        plot_input = name of the PlotPanel's plotter input to be changed by clicking the radio buttons
        data_values = list of possible values to populate the radio button list
    """
    def __init__(self, html_id, parent_id, header, control_type, plot_input, data_values):
        self.plot_input = plot_input
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
            html_id=html_id,
            parent_id=parent_id,
            header=header,
            control_type=control_type,
            component=component,
            component_inputs=component_inputs
        )

    # Overrides parent method
    def panel_transform(self, dp, control_value):
        """
        Changes the PlotPanel's plotting behavior to reflect the user choice.
        """
        dp.plot_inputs[self.plot_input] = control_value
