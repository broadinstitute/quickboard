from dash import dcc, ctx, callback
from dash import dash_table
from dash.dependencies import Input, Output, State, ALL

from quickboard.base import DynamicPanel


class DataPanel(DynamicPanel):
    """
    A dynamic panel meant to hold a Dash DataTable.
    Inputs:
        data_source = where data_manager should look for data; must be either DataFrame, file path, or list of PlotPanel
        and string of one of hoverData, clickData, or selectedData for interactive data generation
        header = header text/object
        body = text/objects to present between header and main_content
        plugins = list of plugin objects to load under main_content to use to manipulate main object
        plugin_wrap = number of plugins to load per row underneath main object
        full_border_size = size of border around entire object
        all_contents_border_size = size of border around all contents
        dynamic_content_border_size = size of border around dynamic content
        plugin_border_size = size of border around plugin group
    """
    def __init__(self, data_source="data", header="", body="", plugins=[], plugin_align="bottom", plugin_wrap=2,
                 full_border_size=0, all_contents_border_size=2, dynamic_content_border_size=0, plugin_border_size=0):
        self.datatable = dash_table.DataTable(
            page_action='none',
            sort_action='native',
            filter_action='native',
            fixed_rows={'headers': True},
            style_table={'overflow': 'auto', 'width': '100%', 'height': '275px'}
        )

        super().__init__(
            header=header,
            body=body,
            dynamic_content=self.datatable,
            data_source=data_source,
            plugins=plugins,
            plugin_align=plugin_align,
            plugin_wrap=plugin_wrap,
            full_border_size=full_border_size,
            all_contents_border_size=all_contents_border_size,
            dynamic_content_border_size=dynamic_content_border_size,
            plugin_border_size=plugin_border_size
        )

        # Table update callback
        dm = self.data_manager
        interactive_data = []
        if dm.source_type == "PlotPanel":
            graph = dm.data_source[0].graph
            plot_data = dm.data_source[1]
            interactive_data = Input(graph, plot_data)
        else:
            interactive_data = Input('data_store', 'data')

        callback(
            Output(self.datatable, 'data'),
            Output(self.datatable, 'columns'),
            Input('data_store', 'data'),
            interactive_data,
            [Input(x.control, 'value') for x in self.plugins if hasattr(x, 'control')]
        )(self.update_table)

    def update_table(self, data_state, interactive_data={}, *control_values):
        """
        A method called to populate the table when the state of a control object is changed.
        """
        sub_df, updated_panel = self.apply_sidebar_transforms(data_state)
        df, panel_dict = self.apply_transforms(ctx, interactive_data, sub_df, control_values)
        updated_panel = dict(updated_panel, **panel_dict)

        data = df.to_dict('records')
        columns = [{'id': c, 'name': c} for c in df.columns]
        return data, columns
