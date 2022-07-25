from dash import html

import pandas as pd

import quickboard.styles as styles
from quickboard.base import ContentGrid
from quickboard.primitives import Panel
from quickboard.primitives import DataManager

from quickboard.plugins import *

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

    def apply_sidebar_transforms(self, data_state):
        """
        A method that is called when sidebar controls are toggled to update the data_state. Performs appropriate data
        and DP transforms before individual plugin transform as applied.
        """
        sidebar_controls = data_state['sidebar_controls']
        sub_df = self.data_manager.df
        updated_panel = {}
        for c in sidebar_controls:
            classname, control_attributes, control_value = c
            config = eval(f"{classname}.configure")
            sub_df, panel_dict = config(control_attributes, self, sub_df, control_value)
            updated_panel = self.merge_dicts(updated_panel, panel_dict)
        return sub_df, updated_panel

    def apply_transforms(self, context, interactive_data={}, df=pd.DataFrame(), control_values=[]):
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
            target_data = dm.data_source[0].data_manager.df
            dm.df = target_data.loc[indices, :]
            df = dm.df

        # Find control plugin objects corresponding to the controls for this plot panel
        controls = [plugin for plugin in self.plugins if hasattr(plugin, 'control')]

        # Apply control plugin effects
        updated_panel = {}
        for control, control_value in zip(controls, control_values):
            df, panel_dict = control.configure(control.control_attributes, self, df, control_value)
            updated_panel = self.merge_dicts(updated_panel, panel_dict)

        df = self.data_transform(df)

        return df, updated_panel

    @staticmethod
    def merge_dicts(d1, d2):
        """
        Handle merging two dictionaries with dictionaries as values, as done in callback loop.
        """
        new_dict = {}
        new_dict.update(d1)
        new_dict.update(d2)
        for k in d1.keys() & d2.keys():
            new_dict[k] = dict(d1[k], **d2[k])

        return new_dict
