from dash import dcc

from quickboard.primitives import ControlPlugin


class Slider(ControlPlugin):
    """
    Template for creating slider plugins.
    Inputs:
        slider_min = the minimal value of the slider
        slider_max = the maximal value of the slider
        slider_default_value = the value the slider starts on by default
        slider_step = controls how granular the slider will be; the minimal change in the slider value when dragging
        slider_marks = dictionary of the form `{num: label}` where position `num` on slider gets label `label`
        tooltip = dictionary with keys 'always_visible' (w/ value = bool) and 'placement' (w/ value = e.g. 'left',
            'right', 'top', etc) to control if selected value should appear on hover; leave blank for no tooltip
        updatemode = either 'mouseup' (default) or 'drag' to specify when data should be updated
        header = header text/object
    """
    def __init__(self, slider_min, slider_max, slider_default_value=None, slider_step=None,
                 slider_marks={}, tooltip={}, updatemode='mouseup', header=""):
        component = dcc.Slider

        default_value = slider_default_value if slider_default_value is not None else slider_max

        component_inputs = {
            'min': slider_min,
            'max': slider_max,
            'value': default_value,
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