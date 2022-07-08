from dash import html

import pandas as pd

import quickboard.styles as styles
from quickboard.base import ContentGrid
from quickboard.base import Panel
from quickboard.base import DataManager


class DynamicPanel(Panel):
    """
    A template for creating larger panels holding objects which can be updated via different controls and plugins.
    Inputs:
        header = header text/object
        main_content = main HTML object to hold
        data_source = key to use in tab data dictionary to get data inputs for this panel
        body = text/objects to present between header and main_content
        plugins = list of plugin objects to load under main_content to use to manipulate main object
        plugin_wrap = number of plugins to load per row underneath main object
        kwargs = extra keyword arguments become attributes of the object for extending functionality easily
    """
    def __init__(self, header, main_content, data_source="data", body="", plugins=[], plugin_wrap=2, **kwargs):
        super().__init__(header, main_content, **kwargs)
        self.data_manager = DataManager(data_source)
        self.data_manager.load_data()

        # Keep list of self as DynamicPanel to register it with larger objects holding it for tab-level callbacks
        self.dps = [self]

        # Add optional body text above main content under header
        self.body = html.Div([body, html.Br()])

        self.main_content = html.Div([main_content], style={'border-width': '1px', 'border-style': 'solid',
                                                            'border-color': 'black'})

        # Configure plugin related attributes
        self.plugins = plugins
        border = False if len(plugins) == 0 else True
        self.plugin_frame = ContentGrid(header="", entities=plugins, col_wrap=plugin_wrap, border=border)

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

    def apply_transforms(self, context, interactive_data={}, control_values=[]):
        """
        A method that is called when relevant control objects change state to manipulate data source before
        passing to the main object.
        """
        dm = self.data_manager

        # Get source of callback trigger
        cb_trigger = context.triggered[0]['prop_id'].split('.')[-1]
        plot_data_types = ['hoverData', 'clickData', 'selectedData']
        if (dm.source_type == "PlotPanel") & (cb_trigger in plot_data_types):
            # Case where plot data selected to trigger callback
            indices = dm.get_interactive_indices(interactive_data)
            target_data = dm.data_source[0].data_manager.sub_df
            dm.df = target_data.loc[indices, :]
            dm.sub_df = target_data.loc[indices, :]

        df = dm.sub_df
        df = self.data_transform(df)

        # Find control plugin objects corresponding to the controls for this plot panel
        controls = [plugin for plugin in self.plugins if hasattr(plugin, 'control')]

        # Apply control plugin effects
        for control, control_value in zip(controls, control_values):
            df = control.configure(self, df, control_value)

        return df
