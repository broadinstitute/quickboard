from quickboard.plugins.templates.slider import Slider


class DataFilterSlider(Slider):
    """
    A plugin for filtering data to be displayed by removing records where a certain column's value does not lie in
    the range specified by the slider.
    Inputs:
        data_col = column from data to restrict values from slider; must be numerical
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
    def __init__(self, data_col, slider_min, slider_max, slider_default_value=None, slider_step=None,
                 slider_marks={}, tooltip={}, updatemode='mouseup', header=""):
        super().__init__(
            slider_min=slider_min,
            slider_max=slider_max,
            slider_default_value=slider_default_value,
            slider_step=slider_step,
            slider_marks=slider_marks,
            tooltip=tooltip,
            updatemode=updatemode,
            header=header
        )

        self.control_attributes = {
            'data_col': data_col,
            'slider_min': slider_min,
            'slider_max': slider_max
        }

    @staticmethod
    def configure(control_attributes, dp, df, control_value):
        """
        Filters data so given column takes value chosen from the slider.
        """
        data_col = control_attributes['data_col']
        df = df[df[data_col] == control_value]

        return df, {}
