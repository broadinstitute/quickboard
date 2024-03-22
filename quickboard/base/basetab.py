from dash import dcc
from dash import html
import quickboard.styles as styles


class BaseTab(html.Div):
    """
    The basic class for creating tabs in an app.
    Inputs:
        tab_label = name appearing on tab button, and used to reference tab elsewhere
        tab_header = opening text at top of tab page
        content_list = list of objects to display on the tab
        sidebar_header = header to use on top of sidebar while on this tab
        sidebar_plugins = plugins to use in the sidebar while on this tab
        sidebar_width = width to use for sidebar style on this tab
    """
    def __init__(self, tab_label, tab_header="", content_list=[], sidebar_header="Data Controls", sidebar_plugins=[],
                 sidebar_width="18rem"):
        self.tab_label = tab_label
        self.tab = dcc.Tab(value=tab_label, label=tab_label)
        self.content_list = content_list
        self.sidebar_header = sidebar_header
        self.sidebar_plugins = sidebar_plugins
        self.sidebar_width = sidebar_width

        for plugin in self.sidebar_plugins:
            if hasattr(plugin, 'control'):
                plugin.control.id = {
                    'control_type': 'sidebar_control',
                    'unique_id': id(plugin)
                }
                plugin.setup_internal_callback()

        for i in range(len(content_list) - 1):
            content_list.insert(2 * i + 1, html.Br())

        self.children = [html.H1(tab_header, style=styles.TAB_HEADER_STYLE)] + self.content_list
        super().__init__(children=self.children)
