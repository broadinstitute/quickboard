from dash import dcc

from quickboard.primitives import ControlPlugin


class RangeSlider(ControlPlugin):
    """
    Template for creating range slider plugins.
    Inputs:
        slider_min = the minimal value of the slider
        slider_max = the maximal value of the slider
        slider_default_values = the values the slider starts on by default; must be a list/tuple of two values
        slider_step = controls how granular the slider will be; the minimal change in the slider value when dragging
        slider_marks = dictionary of the form `{num: label}` where position `num` on slider gets label `label`
        tooltip = dictionary with keys 'always_visible' (w/ value = bool) and 'placement' (w/ value = e.g. 'left',
            'right', 'top', etc) to control if selected value should appear on hover; leave blank for no tooltip
        updatemode = either 'mouseup' (default) or 'drag' to specify when data should be updated
        edges_infinite = when True, consider edges of slider as evaluating to infinity, i.e. no restriction imposed
            on that end; useful for ending a slider with label like '10+'
        header = header text/object
    """
    def __init__(self, slider_min, slider_max, slider_default_values=None, slider_step=None,
                 slider_marks={}, tooltip={}, updatemode='mouseup', edges_infinite=False, header=""):
        component = dcc.RangeSlider

        default_values = slider_default_values if slider_default_values is not None else [slider_min, slider_max]

        component_inputs = {
            'min': slider_min,
            'max': slider_max,
            'value': default_values,
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