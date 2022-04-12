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
        html_id = unique name for this component
        sidebar_header = header text/object to use if no tabs
        sidebar_plugins = list of plugins to use in sidebar if no tabs
        tab_list = list of tab objects from which the board is comprised
        global_contents = objects to display in the absence of tabs
        data_paths = dictionary of `{tab label: paths}` where `paths` is either string or dictionary of
                    `{data source name: path}` to be reference in dynamic panels within the given tab
    """
    def __init__(self, html_id="Dashboard", sidebar_header="Data Controls", sidebar_plugins=[], tab_list=[],
                 global_contents=[], data_paths={}):
        self.html_id = html_id

        # Parse data paths
        self.data_paths = {}
        if isinstance(data_paths, str):
            for tab in tab_list:
                self.data_paths[tab.tab_label] = data_paths
        elif isinstance(data_paths, dict):
            self.data_paths = data_paths
        else:
            print("ERROR: Data paths must be either const string or dictionary of tab_label -> paths.")

        if len(tab_list) != 0:
            first_tab = tab_list[0]
            self.sidebar = Sidebar(html_id + '_Sidebar', first_tab.sidebar_header, first_tab.sidebar_plugins)
        else:
            self.sidebar = Sidebar(html_id + '_Sidebar', sidebar_header, sidebar_plugins)

        # Collect tabs together unless user inputs none
        self.tab_list = tab_list
        if len(tab_list) != 0:
            self.tabs = html.Div(
                children=[dcc.Tabs(
                    id=self.html_id + '_Tabs',
                    value=self.tab_list[0].tab_label,
                    children=[x.tab for x in self.tab_list]
                ),
                    html.Div(id='current_tab_content', children=html.P('If this message persists, then there was '
                                                                       'an ERROR initializing tabs!'))
                ])

            self.current_tab = self.tab_list[0]
            self.tab_dict = {
                tab.tab_label: tab for tab in tab_list
            }
        else:
            self.tabs = html.Div([])

        # Used in case user doesn't want to have tabs, but one page with global contents
        self.global_contents = html.Div(global_contents)

        self.container = html.Div(
            children=[
                self.sidebar.container,
                self.global_contents,
                self.tabs
            ],
            style=styles.CONTENT_STYLE
        )

        #############
        # CALLBACKS #
        #############

        # Add callback for tab switching
        if len(tab_list) > 0:
            app.callback(
                Output('current_tab_content', 'children'),
                Input(self.html_id + '_Tabs', 'value')
            )(self.set_tab)

        # Add callback for managing sidebar layout per tab
            app.callback(
                Output(self.sidebar.html_id + '_Container', 'children'),
                Input(self.html_id + '_Tabs', 'value')
            )(self.update_sidebar_layout)

        # Add callback for updating data from sidebar events
        app.callback(
            Output('data_store', 'data'),
            Input({'type': 'sidebar_control', 'html_id': ALL, 'parent_id': ALL}, 'value'),
            State({'type': 'sidebar_control', 'html_id': ALL, 'parent_id': ALL}, 'id'),
            State(self.html_id + '_Tabs', 'value'),
        )(self.update_data)

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

    def update_data(self, control_values=[], control_ids=[], tab_name=""):
        """
        Callback method handling changes in current tab data sources. Can be triggered by either:
            change in current tab;
            interacting with sidebar plugins.
        """
        new_data_paths = self.data_paths[tab_name]

        # If just one string is passed for tab data, convert to simple dict for downstream compatability
        if isinstance(new_data_paths, str):
            new_dict = {}
            new_dict['data'] = new_data_paths
            new_data_paths = new_dict

        def df_from_path(path):
            if path == '':
                return pd.DataFrame({})
            elif path.split('.')[-1] == 'tsv':
                return pd.read_csv(path, sep='\t')
            else:
                return pd.read_csv(path)

        # Read in dfs relevant to the current tab
        new_dfs = {x: df_from_path(y) for x, y in zip(new_data_paths.keys(), new_data_paths.values())}

        # Find control plugin objects corresponding to the controls for the sidebar
        control_html_ids = [x['html_id'] for x in control_ids]
        controls = [plugin for plugin in self.current_tab.sidebar_plugins if
                    plugin.full_html_id['html_id'] in control_html_ids]

        # Apply control plugin effects
        for control, control_value in zip(controls, control_values):
            for data_source in new_dfs:
                for dp in self.current_tab.dps:
                    new_dfs[data_source] = control.configure(dp, new_dfs[data_source], control_value)

        df_dicts = {x: df.to_dict('records') for x, df in zip(new_dfs.keys(), new_dfs.values())}

        return df_dicts
