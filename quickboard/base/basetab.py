from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from quickboard.dashsetup import app
import quickboard.styles as styles


class BaseTab:
    """
    The basic class for creating tabs in an app.
    Inputs:
        tab_label = name appearing on tab button, and used to reference tab elsewhere
        tab_header = opening text at top of tab page
        content_list = list of objects to display on the tab
        sidebar_header = header to use on top of sidebar while on this tab
        sidebar_plugins = plugins to use in the sidebar while on this tab
    """
    def __init__(self, tab_label, tab_header, content_list, sidebar_header="Data Controls", sidebar_plugins=[]):
        self.tab_label = tab_label
        self.tab = dcc.Tab(value=tab_label, label=tab_label)
        self.sidebar_header = sidebar_header
        self.sidebar_plugins = sidebar_plugins

        for plugin in self.sidebar_plugins:
            if hasattr(plugin, 'control'):
                plugin.control.id = {
                    'control_type': 'sidebar_control',
                    'unique_id': id(plugin)
                }

        # Collect dynamic panels from all subobjects into one place
        self.dps = []
        for entity in content_list:
            if hasattr(entity, 'dps'):
                self.dps += entity.dps

        content_containers = [x.container for x in content_list]
        for i in range(len(content_containers) - 1):
            content_containers.insert(2 * i + 1, html.Br())

        self.container = html.Div(
            [html.H1(tab_header, style=styles.TAB_HEADER_STYLE)] + content_containers,
        )
