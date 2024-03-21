from quickboard.plugins.templates import RadioButtons


class PlotInputRadioButtons(RadioButtons):
    """
    A plugin for modifying a PlotPanel's plotting behavior. The `plot_input` value can be dynamically changed based on
    the selection via radio buttons.
    Inputs:
        plot_input = name of the PlotPanel's plotter input to be changed by clicking the radio buttons
        data_values = list of possible values to populate the radio button list
        header = header text/object
    """
    def __init__(self, plot_input, data_values, header=""):
        super().__init__(
            header=header,
            data_values=data_values
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
