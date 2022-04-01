from dash import dcc

from quickboard.base import ControlPlugin


class DataFilterRadioButtons(ControlPlugin):
    """
    A plugin for filtering data to be displayed by removing records where a certain column's value does not equal the
    selected radio button value.
    Inputs:
        html_id = unique name for this component
        parent_id = html_id of the parent object holding this plugin
        header = header text/object
        control_type = must be either 'plot_control', 'data_control', or 'sidebar_control' depending on where it appears
        data_col = column from data to check for values matching button
        data_values = list of possible values to populate the radio button list
    """
    def __init__(self, html_id, parent_id, header, control_type, data_col, data_values):
        self.data_col = data_col
        component = dcc.RadioItems
        component_inputs = {
            'options': [
                {'label': x, 'value': x} for x in data_values
            ],
            'value': data_values[0],
            'labelStyle': {'display': 'block'},
            'inputStyle': {"margin-right": '10px'}
        }

        super().__init__(
            html_id=html_id,
            parent_id=parent_id,
            header=header,
            control_type=control_type,
            component=component,
            component_inputs=component_inputs
        )

    # Overrides parent method
    def data_transform(self, df, control_value):
        """
        Filters the data by checking the column has value matching the selected button.
        """
        df = df[df[self.data_col] == control_value]
        return df
