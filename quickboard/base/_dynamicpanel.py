from dash import html, dcc

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
        dynamic_content = main HTML object to hold
        data_source = key to use in tab data dictionary to get data inputs for this panel
        header = header text/object
        body = text/objects to present between header and main_content
        plugins = list of plugin objects to load under main_content to use to manipulate main object
        plugin_align = placement of plugins; either bottom, top, left, or right
        plugin_wrap = number of plugins to load per row in plugin grid
        full_border_size = size of border around entire object
        all_contents_border_size = size of border around all contents
        dynamic_content_border_size = size of border around dynamic content
        plugin_border_size = size of border around plugin group
    """
    def __init__(self, dynamic_content, data_source="data", header="", body="", plugins=[], plugin_align="bottom", plugin_wrap=2,
                 full_border_size=0, all_contents_border_size=2, dynamic_content_border_size=0, plugin_border_size=0):
        self.data_manager = DataManager(data_source)
        self.data_manager.load_data()

        self.header = html.H3(header, style=styles.PANEL_HEADER_STYLE) if type(header) == str else header

        # Add optional body text above main content under header
        self.body = html.Div([dcc.Markdown(body, mathjax=True)])

        self.dynamic_content = Panel(main_content=dynamic_content, border_size=dynamic_content_border_size)

        # Configure plugin related attributes
        self.plugins = plugins
        self.plugin_frame = ContentGrid(header="", content_list=plugins, col_wrap=plugin_wrap, border_size=plugin_border_size)

        # Control placement of plugins relative to content
        assert plugin_align in ["bottom", "top", "left", "right"]
        full_wrap = 1 if plugin_align == "bottom" or plugin_align == "top" else 2
        full_content = [self.plugin_frame, self.dynamic_content] if plugin_align in ["top", "left"] else [self.dynamic_content, self.plugin_frame]
        full_content_widths = [25, 100] if plugin_align == "left" else [100, 25] if plugin_align == "right" else []
        self.full_content_grid = ContentGrid(header="", content_list=full_content, content_widths=full_content_widths, col_wrap=full_wrap, border_size=all_contents_border_size)

        self.children = [
            self.header,
            self.body,
            html.Br(),
            self.full_content_grid
        ]
        super().__init__(main_content=self.children, border_size=full_border_size)

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
