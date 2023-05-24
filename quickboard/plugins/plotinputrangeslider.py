from dash import dcc

from quickboard.primitives import ControlPlugin


class PlotInputRangeSlider(ControlPlugin):
    """
    A plugin for toggling a plotter's input using a range of values on a sliding scale.
    Inputs:
        plot_input = name of the PlotPanel's plotter input to be changed by slider
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
    def __init__(self, plot_input, slider_min, slider_max, slider_default_values=None, slider_step=None,
                 slider_marks={}, tooltip={}, updatemode='mouseup', header="", **kwargs):
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
            'plot_input': plot_input,
        }

    @staticmethod
    def configure(control_attributes, dp, df, control_value):
        """
       Updates a PlotPanel's plot_inputs attribute to have new value equal to that selected by slider.
        """
        plot_input = control_attributes['plot_input']
        update = {plot_input: control_value}

        return df, {'plot_inputs': update}
