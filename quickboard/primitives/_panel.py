from dash import html

import quickboard.styles as styles


class Panel(html.Div):
    """
    An "abstract" class representing a panel holding a single Dash/HTML object.
    Inputs:
        header = header text/object
        main_content = main HTML object to hold
    """
    def __init__(self, header, main_content):
        self.header = html.H3(header, style=styles.PANEL_HEADER_STYLE) if type(header) == str else header
        self.main_content = main_content if isinstance(main_content, list) else [main_content]

        self.children = [self.header] + self.main_content
        self.style = styles.PANEL_STYLE
        super().__init__(children=self.children)
