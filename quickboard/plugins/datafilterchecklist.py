from dash import dcc

from quickboard.base import ControlPlugin


class DataFilterChecklist(ControlPlugin):
    """
    A plugin for filtering data to be displayed by removing records where a certain column's value is not in checklist.
    Inputs:
        html_id = unique name for this component
        parent_id = html_id of the parent object holding this plugin
        header = header text/object
        control_type = must be either 'plot_control', 'data_control', or 'sidebar_control' depending on where it appears
        data_col = column from data to check for values in checklist
        data_values = list of possible values to populate the checklist
    """
    def __init__(self, html_id, parent_id, header, control_type, data_col, data_values, **kwargs):
        self.data_col = data_col
        component = dcc.Checklist
        component_inputs = {
            'options': [
                {'label': x, 'value': x} for x in data_values
            ],
            'value': data_values,
            'labelStyle': {'display': 'block'},
            'inputStyle': {"margin-right": '10px'}
        }

        super().__init__(
            html_id=html_id,
            parent_id=parent_id,
            header=header,
            control_type=control_type,
            component=component,
            component_inputs=component_inputs,
            **kwargs
        )

    # Overrides parent method
    def data_transform(self, df, control_value):
        """
        Filters the data by checking the column has values in the currently checked values.
        """
        df = df[df[self.data_col].isin(control_value)]
        return df
