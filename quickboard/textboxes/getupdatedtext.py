from dash import html, callback
from dash.dependencies import Input, Output, State, ALL

import pandas as pd


class GetUpdatedText:
    """
    A textbox that can be populated with the value of another dynamic object's state. Used to make dynamic text
    descriptions.
    Inputs:
        target_component = dynamic object to listen to
        target_prop = property of above object to listen for
        start_text = static text to use before the dynamic text
        end_text = static text to use after the dynamic text
    """
    def __init__(self, target_component, target_prop, start_text, end_text):
        self.textbox = html.Div([])
        self.start_text = start_text
        self.end_text = end_text

        callback(
            Output(self.textbox, 'children'),
            Input(target_component, target_prop)
        )(self.get_update)

    def get_update(self, property):
        return f"{self.start_text}{property}{self.end_text}"


class GetDataTableSize(GetUpdatedText):
    """
    A special case of GetUpdatedText to produce the size of a dynamic DataTable.
    """
    def __init__(self, target_component, start_text, end_text):
        target_prop = 'data'
        super().__init__(target_component, target_prop, start_text, end_text)

    def get_update(self, data):
        df = pd.DataFrame.from_records(data)
        return f"{self.start_text}{len(df)}{self.end_text}"


class GetUpdatedControlValue(GetUpdatedText):
    """
    A special case of GetUpdatedText to produce the value of given object (e.g. checklist, radio buttons, etc).
    """
    def __init__(self, target_component, start_text, end_text):
        target_prop = 'value'
        super().__init__(target_component, target_prop, start_text, end_text)
