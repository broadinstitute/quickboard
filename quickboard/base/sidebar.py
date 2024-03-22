from dash import html

import quickboard.styles as styles


class Sidebar(html.Div):
    """
    An HTML object for creating a sidebar on the left of the screen, used to control data and dynamic panels on the
    current tab page.
    Inputs:
        header_text = header text/object
        sidebar_plugins = plugins to use in the sidebar if there are no tabs in app
    """

    def __init__(self, header_text='Data Controls', sidebar_plugins=[]):
        self.header = [html.H2(header_text, className="display-4"), html.Hr()]
        self.plugins = sidebar_plugins
        # for plugin in self.plugins:
        #     plugin.setup_internal_callback()

        self.children = self.header + self.plugins
        self.style = styles.SIDEBAR_STYLE
        super().__init__(children=self.children)
