from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import quickboard.styles as styles
from quickboard.base import Panel


class ControlPlugin(Panel):
    """
    Creates an HTML component representing controls for a DynamicPanel, as a plugin.
    Inputs:
        html_id = unique name for this component
        parent_id = required for plot controls to work; the html_id of the plot panel holding this plugin
        header = header text/object
        control_type = must be one of 'plot_control' or 'sidebar_control', depending on location of plugin
        component = component from dcc or similar
        component_inputs = the inputs to set up the component
    """

    def __init__(self, html_id, parent_id, header, control_type, component, component_inputs, **kwargs):

        # Calibrate header based on input and control type
        if isinstance(header, str):
            if control_type == 'plot_control':
                header = html.H5(header)
            elif control_type == 'sidebar_control':
                header = html.H3(header)
        else:
            header = header

        self.full_html_id = {
            'type': control_type,
            'html_id': html_id,
            'parent_id': parent_id
        }

        component_inputs.update({'id': self.full_html_id})
        self.control = component(**component_inputs)
        super().__init__(header=header, main_content=self.control, **kwargs)

    def data_transform(self, df, control_value):
        """
        A method for transforming the data to be used in the parent object; called when the control object is changed.
        """
        return df

    def panel_transform(self, dp, control_value):
        """
        A method for transforming the parent DynamicPanel to modify its attributes; called when the control object
        is changed.
        """
        pass

    def configure(self, dp, df, control_value):
        """
        Manipulates the DataFrame and DynamicPanel associated with the plugin according to the transform attributes of
        the plugin. Always returns transformed dataframe for further filtering without needing to serialize when passing
        between components, but modifies DPs "in place".
        """
        df = self.data_transform(df, control_value)
        self.panel_transform(dp, control_value)

        return df
