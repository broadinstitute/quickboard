from dash import dcc, html, ctx, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from quickboard.primitives import ControlPlugin
from dash.dependencies import Input, Output

class Checklist(ControlPlugin):
    """
    Template for creating checklist plugins.
    Inputs:
        data_values = list of possible values to populate the checklist
        header = header text/object
        toggle_all_button = determines whether to include a "toggle all" button with checklist
    """
    def __init__(self, data_values, header="", toggle_all_button=True):
        component = dcc.Checklist
        component_inputs = {
            'options': [
                {'label': x, 'value': x} for x in data_values
            ],
            'value': data_values,
            'labelStyle': {'display': 'block'},
            'inputStyle': {"margin-right": '10px'}
        }

        if toggle_all_button:
            self.all_button = dbc.Button('All', color='primary', className='me-md-2', style={'margin-bottom': '10px'})
            self.none_button = dbc.Button('None', color='dark', className='me-md-2', style={'margin-bottom': '10px'})
            extra_top_content = [
                self.all_button,
                self.none_button,
                html.Br()
            ]
            self.contains_toggle = True
        else:
            extra_top_content = []
            self.contains_toggle = False

        super().__init__(
            header=header,
            component=component,
            component_inputs=component_inputs,
            extra_top_content=extra_top_content
        )

    # Overrides parent method
    def setup_internal_callback(self):
        if self.contains_toggle:
            callback(
                Output(self.control, 'value'),
                Input(self.all_button, 'n_clicks'),
                Input(self.none_button, 'n_clicks')
            )(self.toggle_selection)

    def toggle_selection(self, all_button_clicks, none_button_clicks):
        button_clicked = ctx.triggered_id

        if button_clicked == self.all_button.id:
            return [d['value'] for d in self.control.options]
        elif button_clicked == self.none_button.id:
            return []
        elif button_clicked == None:
            # Prevents updating when first loading page to avoid error with None button clicks
            raise PreventUpdate
        else:
            # Should never be reached
            raise ValueError(f"Invalid button: {button_clicked}")
