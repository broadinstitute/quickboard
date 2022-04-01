from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import quickboard.styles as styles


class BaseTab:
    """
    The basic class for creating tabs in an app.
    Inputs:
        html_id = unique name for this component
        tab_label = name appearing on tab button, and used to reference tab elsewhere
        tab_header = opening text at top of tab page
        content_list = list of objects to display on the tab
        sidebar_header = header to use on top of sidebar while on this tab
        sidebar_plugins = plugins to use in the sidebar while on this tab
    """
    def __init__(self, html_id, tab_label, tab_header, content_list, sidebar_header="Data Controls",
                 sidebar_plugins=[]):
        self.html_id = html_id
        self.tab_label = tab_label
        self.tab = dcc.Tab(id=self.html_id, value=tab_label, label=tab_label)
        self.sidebar_header = sidebar_header
        self.sidebar_plugins = sidebar_plugins

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
