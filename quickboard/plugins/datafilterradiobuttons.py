from quickboard.plugins.templates import RadioButtons


class DataFilterRadioButtons(RadioButtons):
    """
    A plugin for filtering data to be displayed by removing records where a certain column's value does not equal the
    selected radio button value.
    Inputs:
        data_col = column from data to check for values matching button
        data_values = list of possible values to populate the radio button list
        header = header text/object
    """
    def __init__(self, data_col, data_values, header=""):
        super().__init__(
            header=header,
            data_values=data_values
        )

        self.control_attributes = {'data_col': data_col}

    # Overrides parent method
    @staticmethod
    def configure(control_attributes, dp, df, control_value):
        """
        Filters the data by checking the column has value matching the selected button.
        """
        data_col = control_attributes['data_col']
        df = df[df[data_col] == control_value]
        return df, {}
