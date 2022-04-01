from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import pandas as pd

import quickboard.styles as styles
from quickboard.base import ContentGrid


class Panel:
    """
    An "abstract" class representing a panel holding a single Dash/HTML object.
    Inputs:
        header = header text/object
        main_content = main HTML object to hold
        kwargs = extra keyword arguments become attributes of the object for extending functionality easily
    """
    def __init__(self, header, main_content, **kwargs):
        self.header = html.H3(header, style=styles.PANEL_HEADER_STYLE) if type(header) == str else header
        self.main_content = main_content

        self.container = dbc.Toast([
            self.header, self.main_content
        ],
            style=styles.PANEL_STYLE
        )

        for key, value in kwargs.items():
            setattr(self, key, value)


class DynamicPanel(Panel):
    """
    A template for creating larger panels holding objects which can be updated via different controls and plugins.
    Inputs:
        html_id = unique name for this component
        header = header text/object
        main_content = main HTML object to hold
        data_source = key to use in tab data dictionary to get data inputs for this panel
        body = text/objects to present between header and main_content
        plugins = list of plugin objects to load under main_content to use to manipulate main object
        plugin_wrap = number of plugins to load per row underneath main object
        kwargs = extra keyword arguments become attributes of the object for extending functionality easily
    """
    def __init__(self, html_id, header, main_content, data_source="data", body="", plugins=[], plugin_wrap=2, **kwargs):
        super().__init__(header, main_content, **kwargs)

        self.html_id = html_id
        self.full_html_id = {
            'type': 'dyanmic_panel',
            'html_id': html_id,
        }
        self.data_source = data_source

        # Keep list of self as DynamicPanel to register it with larger objects holding it for tab-level callbacks
        self.dps = [self]

        # Add optional body text above main content under header
        self.body = html.Div([body, html.Br()])

        self.main_content = html.Div([main_content], style={'border-width': '1px', 'border-style': 'solid',
                                                            'border-color': 'black'})


        # Configure plugin related attributes
        self.plugins = plugins
        border = False if len(plugins) == 0 else True
        self.plugin_frame = ContentGrid(html_id + '_PluginFrame', header="", entities=plugins,
                                        col_wrap=plugin_wrap, border=border)

        self.container = html.Div([
            self.header, self.body, html.Br(), self.main_content, html.Br(), self.plugin_frame.container
        ],
            style=styles.PANEL_STYLE
        )

    def data_transform(self, df):
        """
        A method for applying specific transformations to the data source before passing to main object, regardless
        of control object states.
        """
        return df

    def apply_transforms(self, data_state, control_values=[], control_ids=[]):
        """
        A method that is called when relevant control objects change state to manipulate data source before
        passing to the main object.
        """
        df = pd.DataFrame.from_records(data_state[self.data_source])
        df = self.data_transform(df)

        # Find control plugin objects corresponding to the controls for this plot panel
        control_html_ids = [x['html_id'] for x in control_ids]
        controls = [plugin for plugin in self.plugins if plugin.full_html_id['html_id'] in control_html_ids]

        # Apply control plugin effects
        for control, control_value in zip(controls, control_values):
            df = control.configure(self, df, control_value)

        return df
