from quickboard.plugins.templates.rangeslider import RangeSlider


class DataFilterRangeSlider(RangeSlider):
    """
    A plugin for filtering data to be displayed by removing records where a certain column's value does not lie in
    the range specified by the slider.
    Inputs:
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
        header = header text/object
    """
    def __init__(self, data_col, slider_min, slider_max, slider_default_values=None, slider_step=None,
                 slider_marks={}, tooltip={}, updatemode='mouseup', edges_infinite=False, header=""):
        super().__init__(
            slider_min=slider_min,
            slider_max=slider_max,
            slider_default_values=slider_default_values,
            slider_step=slider_step,
            slider_marks=slider_marks,
            tooltip=tooltip,
            updatemode=updatemode,
            edges_infinite=edges_infinite,
            header=header
        )

        self.control_attributes = self.control_attributes | {'data_col': data_col}

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
