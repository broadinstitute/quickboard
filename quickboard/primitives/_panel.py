from dash import html

import quickboard.styles as styles


class Panel(html.Div):
    """
    An "abstract" class representing a panel with optional border holding some Dash/HTML objects.
    Inputs:
        main_content = main HTML object to hold
        border_size = integer width in pixel for border
    """
    def __init__(self, main_content, border_size=2):
        # self.header = html.H3(header, style=styles.PANEL_HEADER_STYLE) if type(header) == str else header
        self.main_content = main_content if isinstance(main_content, list) else [main_content]

        self.children = self.main_content
        self.style = styles.PANEL_STYLE
        super().__init__(children=self.children)
        self.update_border_size(border_size)

    def update_border_size(self, size):
        self.style = self.style | {"border-width": f"{size}px"}
        return self
