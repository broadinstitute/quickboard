from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL

import quickboard.styles as styles
from quickboard.dashsetup import app
from quickboard.base import DynamicPanel

import pandas as pd


# Class representing a plot object with surrounding HTML objects
class PlotPanel(DynamicPanel):
    """
    A dynamic panel meant to hold a Plotly figure.
    Inputs:
        html_id = unique name for this component
        header = header text/object
        plotter = function which outputs a Plotly figure
        plot_inputs = dictionary of inputs which is passed to plotter to produce figure
        data_source = key to use in tab data dictionary to get data inputs for this panel
        body = text/objects to present between header and main_content
        plugins = list of plugin objects to load under main_content to use to manipulate main object
        plugin_wrap = number of plugins to load per row underneath main object
        kwargs = extra keyword arguments become attributes of the object for extending functionality easily
    """
    def __init__(self, html_id, header, plotter, plot_inputs, data_source="data", body="", plugins=[], plugin_wrap=2, **kwargs):
        # Plot specific attributes
        self.plot_inputs = plot_inputs
        self.plotter = plotter
        self.graph = dcc.Graph(
            id=html_id
        )

        super().__init__(
            html_id=html_id,
            header=header,
            main_content=self.graph,
            data_source=data_source,
            plugins=plugins,
            body=body,
            plugin_wrap=plugin_wrap,
            **kwargs
        )

        # Plot update callback
        app.callback(
            Output(self.html_id, 'figure'),
            Input('data_store', 'data'),
            Input({'type': 'plot_control', 'html_id': ALL, 'parent_id': self.html_id}, 'value'),
            State({'type': 'plot_control', 'html_id': ALL, 'parent_id': self.html_id}, 'id')
        )(self.make_plot)

    def make_plot(self, data_state, control_values=[], control_ids=[]):
        """
        A method called to create the figure when the state of a control object is changed.
        """
        df = self.apply_transforms(data_state, control_values, control_ids)

        fig = self.plotter(df, **self.plot_inputs)
        fig = self.fig_postprocess(fig, df)

        return fig

    def fig_postprocess(self, fig, df):
        """
        A method called after the Plotly figure has been generated from a change in control state, to allow for
        post-processing manipulations to the final figure which gets displayed.
        """
        return fig
