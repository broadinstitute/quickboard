from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import quickboard.styles as styles
from quickboard.primitives import Panel


class ControlPlugin(Panel):
    """
    Creates an HTML component representing controls for a DynamicPanel, as a plugin.
    Inputs:
        header = header text/object
        component = component from dcc or similar
        component_inputs = the inputs to set up the component
    """

    def __init__(self, header, component, component_inputs, **kwargs):
        self.control_attributes = {}
        # Calibrate header based on input
        if isinstance(header, str):
            header = html.H3(header)
        else:
            header = header

        self.control = component(**component_inputs)
        super().__init__(header=header, main_content=self.control, **kwargs)

    def serialize(self):
        """
        Returns a list with ClassName & control_attributes
        """
        classname = str(type(self)).split('.')[-1].split("'")[0]
        return [classname, self.control_attributes]

    @staticmethod
    def configure(control_attributes, dp, df, control_value):
        """
        Manipulates the DataFrame and DynamicPanel associated with the plugin according to the transform attributes of
        the plugin. Always returns transformed dataframe for further filtering without needing to serialize when passing
        between components and returns a dict of stateful changes to DynamicPanel".
        """
        updated_panel = {}

        return df, updated_panel
