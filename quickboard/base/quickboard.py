from dash import dcc, html, callback
from dash.dependencies import Input, Output, State, ALL

from quickboard.base.sidebar import Sidebar
import quickboard.styles as styles


class Quickboard(html.Div):
    """
    Main class for making an easy dashboard out of modular components. Handles some global dynamic aspects of the
    board while holding all the pieces together.
    Inputs:
        sidebar_header = header text/object to use if no tabs
        sidebar_plugins = list of plugins to use in sidebar if no tabs
        tab_list = list of tab objects from which the board is comprised
        content_list = objects to display in the absence of tabs
    """
    def __init__(self, sidebar_header="Data Controls", sidebar_plugins=[], tab_list=[], content_list=[]):
        self.style = styles.CONTENT_STYLE
        self.tab_list = tab_list
        self.tabs_wrapper = self.initialize_tabs(tab_list)
        self.sidebar = self.initialize_sidebar(sidebar_header, sidebar_plugins)

        # Used in case user doesn't want to have tabs, but one page with some contents
        self.content_list = content_list

        self.children = [
                self.sidebar,
                html.Div(self.content_list),
                self.tabs_wrapper
            ]

        super().__init__(children=self.children)

        #############
        # CALLBACKS #
        #############

        # Add callback for tab switching
        # Handles updating sidebar contents, tab contents, and resizing sidebar margins based on tab properties
        if len(tab_list) > 0:
            callback(
                Output(self.current_tab_content, 'children'),
                Output(self.sidebar, 'children'),
                Output(self.sidebar, 'style'),
                Output(self, 'style'),
                Input(self.tabs, 'value')
            )(self.tab_switch_update)

        # Add callback for updating data from sidebar events
        # Configure input based on whether user input tabs
        update_data_inputs = Input({'control_type': 'sidebar_control', 'unique_id': ALL}, 'value')
        if len(tab_list) > 0:
            update_data_inputs = [update_data_inputs, Input(self.tabs, 'value')]

        callback(
            Output('data_store', 'data'),
            State('data_store', 'data'),
            update_data_inputs,
        )(self.update_data)

    def initialize_tabs(self, tab_list):
        # Collect tabs together unless user inputs none
        if len(tab_list) > 0:
            self.tabs = dcc.Tabs(
                    value=self.tab_list[0].tab_label,
                    children=[x.tab for x in self.tab_list]
            )

            self.current_tab_content = html.Div(children=html.P('If this message persists, then there was an ERROR '
                                                                'initializing tabs!'))

            self.tab_dict = {
                tab.tab_label: tab for tab in tab_list
            }

            tabs_wrapper = html.Div(
                children=[
                    self.tabs,
                    self.current_tab_content
                ]
            )
        else:
            tabs_wrapper = html.Div([])

        return tabs_wrapper

    def initialize_sidebar(self, sidebar_header, sidebar_plugins):
        if len(self.tab_list) > 0:
            first_tab = self.tab_list[0]
            self.sidebar = Sidebar(first_tab.sidebar_header, first_tab.sidebar_plugins)
            return self.sidebar
        elif len(sidebar_plugins) != 0:
            self.sidebar = Sidebar(sidebar_header, sidebar_plugins)

            # Distinguish sidebar plugins for later callback
            for plugin in sidebar_plugins:
                if hasattr(plugin, 'control'):
                    plugin.control.id = {
                        'control_type': 'sidebar_control',
                        'unique_id': id(plugin)
                    }

            return self.sidebar
        else:
            self.style["margin-left"] = "2rem"
            return html.Div([])

    def set_tab(self, tab_name):
        """
        Callback method for updating the current tab, based on user click.
        """
        current_tab = self.tab_dict[tab_name]
        return current_tab

    def update_sidebar_layout(self, tab_name):
        """
        Callback method for updating the sidebar layout corresponding to the current tab.
        """
        current_tab = self.tab_dict[tab_name]
        plugins = current_tab.sidebar_plugins

        # Put hlines between plugins
        hlines = [(plugin, html.Hr()) for plugin in plugins]
        sidebar_layout = [y for sublist in hlines for y in sublist][:-1]

        # Update sidebar width
        width = current_tab.sidebar_width
        new_style = styles.SIDEBAR_STYLE | {'width': width}

        return [self.sidebar.header + sidebar_layout, new_style]

    def tab_switch_update(self, tab_name):
        selected_tab = self.set_tab(tab_name)
        updated_sidebar_layout, updated_sidebar_style = self.update_sidebar_layout(tab_name)

        # Update content margins to match sidebar width
        updated_main_content_style = self.style | {'margin-left': updated_sidebar_style['width']}

        return [selected_tab, updated_sidebar_layout, updated_sidebar_style, updated_main_content_style]

    def update_data(self, data_state={}, control_values=[], tab_name=""):
        """
        Callback method handling changes in current tab data sources. Can be triggered by either:
            change in current tab;
            interacting with sidebar plugins.
        """

        data_state['current_tab'] = tab_name

        # Get sidebar_plugins depending on tab
        if tab_name != "":
            current_tab = self.tab_dict[tab_name]
            sidebar_plugins = current_tab.sidebar_plugins
        else:
            sidebar_plugins = self.sidebar.plugins if hasattr(self.sidebar, 'plugins') else []

        controls = [plugin for plugin in sidebar_plugins if hasattr(plugin, 'control')]
        serialized_controls = [c.serialize() for c in controls]

        # Create list of 3-tuples w/ control class, control attributes, and control values
        control_info = [
            x + [y] for x, y in zip(serialized_controls, control_values)
        ]

        data_state['sidebar_controls'] = control_info
        return data_state
