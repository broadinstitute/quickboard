from dash import dcc

from quickboard.primitives import ControlPlugin


class RangeSlider(ControlPlugin):
    def __init__(self, slider_min, slider_max, slider_default_values=None, slider_step=None,
                 slider_marks={}, tooltip={}, updatemode='mouseup', edges_infinite=False, header=""):
        component = dcc.RangeSlider

        component_inputs = {
            'min': slider_min,
            'max': slider_max,
            'value': slider_default_values,
            'step': slider_step,
            'included': True,
            'marks': slider_marks,
            'tooltip': tooltip,
            'updatemode': updatemode
        }

        super().__init__(
            header=header,
            component=component,
            component_inputs=component_inputs
        )

        self.control_attributes = self.control_attributes | {
            'slider_min': slider_min,
            'slider_max': slider_max,
            'edges_infinite': edges_infinite
        }