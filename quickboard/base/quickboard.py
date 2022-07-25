from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ALL

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
        self.dps = []
        for entity in content_list:
            if hasattr(entity, 'dps'):
                self.dps += entity.dps

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
        update_data_inputs = Input({'control_type': 'sidebar_control', 'unique_id': ALL}, 'value')
        if len(tab_list) > 0:
            update_data_inputs = [update_data_inputs, Input(self.tabs, 'value')]

        app.callback(
            Output('data_store', 'data'),
            State('data_store', 'data'),
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

            # Distinguish sidebar plugins for later callback
            for plugin in sidebar_plugins:
                if hasattr(plugin, 'control'):
                    plugin.control.id = {
                        'control_type': 'sidebar_control',
                        'unique_id': id(plugin)
                    }

            return self.sidebar.container
        else:
            self.style["margin-left"] = "2rem"
            return html.Div([])

    def set_tab(self, tab_name):
        """
        Callback method for updating the current tab, based on user click.
        """
        current_tab = self.tab_dict[tab_name]
        return current_tab.container

    def update_sidebar_layout(self, tab_name):
        """
        Callback method for updating the sidebar layout corresponding to the current tab.
        """
        current_tab = self.tab_dict[tab_name]
        plugins = current_tab.sidebar_plugins
        plugin_containers = [x.container for x in plugins]

        # Put hlines between plugins
        hlines = [(plugin, html.Hr()) for plugin in plugin_containers]
        sidebar_layout = [y for sublist in hlines for y in sublist][:-1]

        return self.sidebar.header + sidebar_layout

    def tab_switch_update(self, tab_name):
        set_tab_container = self.set_tab(tab_name)
        updated_sidebar_layout = self.update_sidebar_layout(tab_name)

        return [set_tab_container, updated_sidebar_layout]

    def update_data(self, data_state={}, control_values=[], tab_name=""):
        """
        Callback method handling changes in current tab data sources. Can be triggered by either:
            change in current tab;
            interacting with sidebar plugins.
        """

        data_state['current_tab'] = tab_name
        current_tab = self.tab_dict[tab_name]

        # Get sidebar_plugins depending on tab
        if tab_name != "":
            sidebar_plugins = current_tab.sidebar_plugins
        else:
            sidebar_plugins = self.sidebar.plugins if hasattr(self, 'sidebar') else []

        controls = [plugin for plugin in sidebar_plugins if hasattr(plugin, 'control')]
        serialized_controls = [c.serialize() for c in controls]

        # Create list of 3-tuples w/ control class, control attributes, and control values
        control_info = [
            x + [y] for x, y in zip(serialized_controls, control_values)
        ]

        data_state['sidebar_controls'] = control_info
        return data_state
