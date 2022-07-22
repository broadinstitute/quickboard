from dash import dcc, ctx
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
        header = header text/object
        plotter = function which outputs a Plotly figure
        plot_inputs = dictionary of inputs which is passed to plotter to produce figure
        data_source = where data_manager should look for data; must be either DataFrame, file path, or list of PlotPanel
        and string of one of hoverData, clickData, or selectedData for interactive data generation
        body = text/objects to present between header and main_content
        plugins = list of plugin objects to load under main_content to use to manipulate main object
        plugin_wrap = number of plugins to load per row underneath main object
        kwargs = extra keyword arguments become attributes of the object for extending functionality easily
    """
    def __init__(self, header, plotter, plot_inputs, data_source="data", body="", plugins=[], plugin_wrap=2, **kwargs):
        # Plot specific attributes
        self.plot_inputs = plot_inputs
        self.plotter = plotter
        self.graph = dcc.Graph()

        super().__init__(
            header=header,
            main_content=self.graph,
            data_source=data_source,
            plugins=plugins,
            body=body,
            plugin_wrap=plugin_wrap,
            **kwargs
        )

        # Plot update callback
        dm = self.data_manager
        interactive_data = []
        if dm.source_type == "PlotPanel":
            graph = dm.data_source[0].graph
            plot_data = dm.data_source[1]
            interactive_data = Input(graph, plot_data)
        else:
            interactive_data = Input('data_store', 'data')

        app.callback(
            Output(self.graph, 'figure'),
            Input('data_store', 'data'),
            interactive_data,
            [Input(x.control, 'value') for x in self.plugins if hasattr(x, 'control')]
        )(self.make_plot)

    def make_plot(self, data_state, interactive_data, *control_values):
        """
        A method called to create the figure when the state of a control object is changed.
        """
        df = self.apply_transforms(ctx, interactive_data, control_values)
        fig = self.plotter(df, **self.plot_inputs)
        return fig
