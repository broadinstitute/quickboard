from dash import dcc

from quickboard.base import ControlPlugin


class DataFilterSlider(ControlPlugin):
    """
    A plugin for filtering data to be displayed by removing records where a certain column's value does not lie in
    the range specified by the slider.
    Inputs:
        html_id = unique name for this component
        parent_id = html_id of the parent object holding this plugin
        header = header text/object
        control_type = must be either 'plot_control', 'data_control', or 'sidebar_control' depending on where it appears
        data_col = column from data to restrict values from slider; must be numerical
        slider_min = the minimal value of the slider
        slider_max = the maximal value of the slider
        slider_default_values = the value(s) the slider starts on by default; if a single number, then slider will be
            one-sided, and data will be restricted to be less than slider value; if a pair (tuple or list) of numbers,
            then slider will be two-sided, and data will be restricted to lie between the two values
        slider_step = controls how granular the slider will be; the minimal change in the slider value when dragging
        slider_marks = dictionary of the form `{num: label}` where position `num` on slider gets label `label`
        edges_infinite = if True, treat the edges of slider as infinite (no restriction on data when min/max)
    """
    def __init__(self, html_id, parent_id, header, control_type, data_col, slider_min, slider_max,
                 slider_default_values, slider_step, slider_marks={}, edges_infinite=True, **kwargs):
        self.data_col = data_col
        self.slider_min = slider_min
        self.slider_max = slider_max
        self.edges_infinite = edges_infinite

        try:
            float(slider_default_values)
            component = dcc.Slider
        except TypeError:
            try:
                tuple(slider_default_values)
                if len(slider_default_values) == 2:
                    component = dcc.RangeSlider
                else:
                    print("ERROR: If using range of defaults, must input a pair.")
            except TypeError:
                print("ERROR: Default values must be either single number or pair of values in list/tuple.")

        # If no marks provided, use the min/max values as only labels
        if slider_marks == {}:
            slider_marks = {slider_min: str(slider_min), slider_max: str(slider_max)}

        component_inputs = {
            'min': slider_min,
            'max': slider_max,
            'value': slider_default_values,
            'step': slider_step,
            'included': True,
            'marks': slider_marks
        }

        super().__init__(
            html_id=html_id,
            parent_id=parent_id,
            header=header,
            control_type=control_type,
            component=component,
            component_inputs=component_inputs
        )

    def data_transform(self, df, control_value):
        """
        Filters data so given column lies within the range of the slider.
        """
        try:
            # Handle case of normal one-sided slider
            float(control_value)
            if self.edges_infinite & (control_value == self.slider_max):
                df = df
            else:
                df = df[df[self.data_col] <= control_value]
        except TypeError:
                try:
                    # Handle case of two-sided slider
                    tuple(control_value)
                    # Left side of slider
                    if self.edges_infinite & (control_value[0] == self.slider_min):
                        df = df
                    else:
                        df = df[df[self.data_col] >= control_value[0]]

                    # Right side of slider
                    if self.edges_infinite & (control_value[1] == self.slider_max):
                        df = df
                    else:
                        df = df[df[self.data_col] <= control_value[1]]
                except TypeError:
                    print("ERROR: Invalid control_value. Expecting single input or list/tuple of slider values.")

        return df
