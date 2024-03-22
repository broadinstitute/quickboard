from dash import html
import dash_bootstrap_components as dbc

import quickboard.styles as styles


class ControlPlugin(dbc.Toast):
    """
    Creates an HTML component representing controls for a DynamicPanel, as a plugin.
    Inputs:
        component = component from dcc or similar
        component_inputs = the inputs to set up the component
        extra_top_content = extra Dash objects to include above main control component
        header = header text/object
    """

    def __init__(self, component, component_inputs, extra_top_content=[], header=""):
        self.control_attributes = {}
        # Calibrate header based on input
        if isinstance(header, str):
            header = html.H3(header)
        else:
            header = header

        self.control = component(**component_inputs)

        self.children = extra_top_content+[self.control]
        self.style = styles.PANEL_STYLE
        super().__init__(
            header=header,
            header_style={'color': '#000000'},
            children=self.children
        )

        self.setup_internal_callback()

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

    def setup_internal_callback(self):
        """
        To be implemented by children classes. Declares callbacks to be used by internal components in the plugin, activated
        later during the app setup to ensure compatibility of ids used. Gets called at end of self init and in Sidebar init.
        """
        pass
