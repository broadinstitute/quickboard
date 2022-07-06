from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL

import pandas as pd

from quickboard.base.sidebar import Sidebar
from quickboard.dashsetup import app
import quickboard.styles as styles


class Quickboard:
    """
    Main class for making an easy dashboard out of modular components. Handles some global dynamic aspects of the
    board while holding all of the pieces together.
    Inputs:
        sidebar_header = header text/object to use if no tabs
        sidebar_plugins = list of plugins to use in sidebar if no tabs
        tab_list = list of tab objects from which the board is comprised
        content_list = objects to display in the absence of tabs
        data_paths = dictionary of `{tab label: paths}` where `paths` is either string or dictionary of
                    `{data source name: path}` to be reference in dynamic panels within the given tab
    """
    def __init__(self, sidebar_header="Data Controls", sidebar_plugins=[], tab_list=[], content_list=[],
                 data_paths={}):
        self.style = styles.CONTENT_STYLE
        self.tabs_container = self.initialize_tabs(tab_list, data_paths)
        self.sidebar_container = self.initialize_sidebar(sidebar_header, sidebar_plugins)

        # Used in case user doesn't want to have tabs, but one page with some contents
        self.content_list = html.Div([x.container for x in content_list])

        self.container = html.Div(
            children=[
                self.sidebar_container,
                self.content_list,
                self.tabs_container
            ],
            style=self.style
        )

        #############
        # CALLBACKS #
        #############

        # Add callback for tab switching
        if len(tab_list) > 0:
            app.callback(
                Output(self.current_tab_content, 'children'),
                Output(self.sidebar_container, 'children'),
                Input(self.tabs, 'value')
            )(self.tab_switch_update)

        # Add callback for updating data from sidebar events
        # Configure input based on whether user input tabs
        update_data_inputs = [Input({'control_type': 'sidebar_control', 'unique_id': ALL}, 'value')]
        update_data_inputs += [Input(self.tabs, 'value')] if tab_list else []  # add only if nonempty tab list
        app.callback(
            Output('data_store', 'data'),
            update_data_inputs,
        )(self.update_data)

    def initialize_tabs(self, tab_list, data_paths):
        # Parse data paths
        self.data_paths = {}
        if isinstance(data_paths, str):
            for tab in tab_list:
                self.data_paths[tab.tab_label] = data_paths
        elif isinstance(data_paths, dict):
            self.data_paths = data_paths
        else:
            print("ERROR: Data paths must be either const string or dictionary of tab_label -> paths.")

        # Collect tabs together unless user inputs none
        self.tab_list = tab_list
        if len(tab_list) != 0:
            self.tabs = dcc.Tabs(
                    value=self.tab_list[0].tab_label,
                    children=[x.tab for x in self.tab_list]
            )

            self.current_tab_content = html.Div(children=html.P('If this message persists, then there was an ERROR '
                                                                'initializing tabs!'))

            self.current_tab = self.tab_list[0]
            self.tab_dict = {
                tab.tab_label: tab for tab in tab_list
            }
            tabs_container = html.Div(
                children=[
                    self.tabs,
                    self.current_tab_content
                ]
            )
        else:
            tabs_container = html.Div([])
        return tabs_container

    def initialize_sidebar(self, sidebar_header, sidebar_plugins):
        if len(self.tab_list) != 0:
            first_tab = self.tab_list[0]
            self.sidebar = Sidebar(first_tab.sidebar_header, first_tab.sidebar_plugins)
            return self.sidebar.container
        elif len(sidebar_plugins) != 0:
            self.sidebar = Sidebar(sidebar_header, sidebar_plugins)
            return self.sidebar.container
        else:
            self.style["margin-left"] = "2rem"
            return html.Div([])

    def set_tab(self, tab_name):
        """
        Callback method for updating the current tab, based on user click.
        """
        self.current_tab = self.tab_dict[tab_name]
        return self.current_tab.container

    def update_sidebar_layout(self, tab_name):
        """
        Callback method for updating the sidebar layout corresponding to the current tab.
        """
        plugins = self.current_tab.sidebar_plugins
        plugin_containers = [x.container for x in plugins]

        # Put hlines between plugins
        hlines = [(plugin, html.Hr()) for plugin in plugin_containers]
        sidebar_layout = [y for sublist in hlines for y in sublist][:-1]

        return self.sidebar.header + sidebar_layout

    def tab_switch_update(self, tab_name):
        set_tab_container = self.set_tab(tab_name)
        updated_sidebar_layout = self.update_sidebar_layout(tab_name)

        return [set_tab_container, updated_sidebar_layout]

    def update_data(self, control_values=[], tab_name=""):
        """
        Callback method handling changes in current tab data sources. Can be triggered by either:
            change in current tab;
            interacting with sidebar plugins.
        """
        new_data_paths = self.data_paths[tab_name]

        # If just one string is passed for tab data, convert to simple dict for downstream compatability
        if isinstance(new_data_paths, str):
            new_data_paths = {'data': new_data_paths}

        def df_from_path(path):
            if path == '':
                return pd.DataFrame({})
            elif path.split('.')[-1] == 'tsv':
                return pd.read_csv(path, sep='\t')
            else:
                return pd.read_csv(path)

        # Read in dfs relevant to the current tab
        new_dfs = {x: df_from_path(new_data_paths[x]) for x in new_data_paths}

        # Find control plugin objects corresponding to the controls for the sidebar
        controls = [plugin for plugin in self.current_tab.sidebar_plugins if hasattr(plugin, 'control')]

        # Apply control plugin effects
        for control, value in zip(controls, control_values):
            for data_source in new_dfs:
                for dp in self.current_tab.dps:
                    new_dfs[data_source] = control.configure(dp, new_dfs[data_source], value)

        df_dicts = {x: new_dfs[x].to_dict('records') for x in new_dfs}
        return df_dicts
