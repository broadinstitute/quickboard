import numpy as np
from dash import dcc

from quickboard.primitives import ControlPlugin


class DataFilterRangeSlider(ControlPlugin):
    """
    A plugin for filtering data to be displayed by removing records where a certain column's value does not lie in
    the range specified by the slider.
    Inputs:
        header = header text/object
        data_col = column from data to restrict values from slider; must be numerical
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
    """
    def __init__(self, header, data_col, slider_min, slider_max, slider_default_values=None, slider_step=None,
                 slider_marks={}, tooltip={}, updatemode='mouseup', edges_infinite=False, **kwargs):
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

        self.control_attributes = {
            'data_col': data_col,
            'slider_min': slider_min,
            'slider_max': slider_max,
            'edges_infinite': edges_infinite
        }

    @staticmethod
    def configure(control_attributes, dp, df, control_value):
        """
        Filters data so given column lies within the range of the slider.
        """
        current_min = control_value[0]
        current_max = control_value[1]

        if control_attributes['edges_infinite']:
            current_min = -np.inf if current_min == control_attributes['slider_min'] else current_min
            current_max = np.inf if current_max == control_attributes['slider_max'] else current_max

        data_col = control_attributes['data_col']
        df = df[(df[data_col] >= current_min) & (df[data_col] <= current_max)]

        return df, {}
