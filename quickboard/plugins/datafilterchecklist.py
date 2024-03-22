from quickboard.plugins.templates import Checklist


class DataFilterChecklist(Checklist):
    """
    A plugin for filtering data to be displayed by removing records where a certain column's value is not in checklist.
    Inputs:
        data_col = column from data to check for values in checklist
        data_values = list of possible values to populate the checklist
        header = header text/object
        toggle_all_button = determines whether to include a "toggle all" button with checklist
    """
    def __init__(self, data_col, data_values, header="", toggle_all_button=True):
        super().__init__(
            data_values=data_values,
            header=header,
            toggle_all_button=toggle_all_button
        )

        self.control_attributes = {'data_col': data_col}

    # Overrides parent method
    @staticmethod
    def configure(control_attributes, dp, df, control_value):
        """
        Filters the data by checking the column has values in the currently checked values.
        """
        data_col = control_attributes['data_col']
        df = df[df[data_col].isin(control_value)]
        return df, {}
