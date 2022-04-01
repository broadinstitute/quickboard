from dash import html
from dash.dependencies import Input, Output, State, ALL

from quickboard.dashsetup import app

import pandas as pd


class GetUpdatedText:
    """
    A textbox that can be populated with the value of another dynamic object's state. Used to make dynamic text
    descriptions.
    Inputs:
        html_id = unique name for this component
        target_id = dynamic object html_id to listen to
        target_prop = property of above object to listen for
        start_text = static text to use before the dynamic text
        end_text = static text to use after the dynamic text
    """
    def __init__(self, html_id, target_id, target_prop, start_text, end_text):
        self.html_id = html_id
        self.textbox = html.Div([], id=html_id)
        self.start_text = start_text
        self.end_text = end_text

        app.callback(
            Output(html_id, 'children'),
            Input(target_id, target_prop)
        )(self.get_update)

    def get_update(self, property):
        return f"{self.start_text}{property}{self.end_text}"


class GetDataTableSize(GetUpdatedText):
    """
    A special case of GetUpdatedText to produce the size of a dynamic DataTable.
    """
    def __init__(self, html_id, target_id, start_text, end_text):
        target_prop = 'data'
        super().__init__(html_id, target_id, target_prop, start_text, end_text)

    def get_update(self, data):
        df = pd.DataFrame.from_records(data)
        return f"{self.start_text}{len(df)}{self.end_text}"


class GetUpdatedControlValue(GetUpdatedText):
    """
    A special case of GetUpdatedText to produce the value of given object (e.g. checklist, radio buttons, etc).
    """
    def __init__(self, html_id, target_id, start_text, end_text):
        target_prop = 'value'
        super().__init__(html_id, target_id, target_prop, start_text, end_text)
