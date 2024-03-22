import plotly.express as px

import quickboard.base as qbb
import quickboard.plugins as plg
from test import TestTemplate


class PlotPanelTest(TestTemplate):
    """
    Tests:
        - Plugins on bottom/top/left/right
        - Sidebar plugins work across multiple plots
        - No tabs edge case
        - Toggle borders on various Panels
        - Test complex layout using ContentGrids
    """

    def make_test_board(self):
        first_row = qbb.ContentGrid(content_list=[
            self.make_test_panel(side="top"),
            self.make_test_panel(side="bottom")
        ])

        second_row = qbb.ContentGrid(content_list=[
            self.make_test_panel("right")
        ]).update_border_size(5)

        third_row = qbb.ContentGrid(content_list=[
            self.make_test_panel("left").update_border_size(1)
        ])

        fourth_row_bottom_plot = self.make_test_panel("bottom")
        fourth_row_bottom_plot.dynamic_content.update_border_size(2)
        fourth_row = qbb.ContentGrid(content_list=[
            fourth_row_bottom_plot,
            self.make_test_panel("top")
        ])

        main_tab = qbb.BaseTab(
            content_list=[
                first_row,
                second_row,
                third_row,
                fourth_row
            ],
            tab_label="Main",
            tab_header="Main tab"
        )

        board = qbb.Quickboard(
            content_list=[
                main_tab
            ],
            sidebar_header="PlotPanel Test",
            sidebar_plugins=[
                plg.DataFilterRangeSlider(
                    header="Data Filter Range Slider Test",
                    data_col='year',
                    slider_min=int(self.df['year'].min()),
                    slider_max=int(self.df['year'].max())
                )
            ]
        )

        return board
        return main_tab

    def make_test_panel(self, side):
        plot_panel = qbb.PlotPanel(
            header=f"Test for Plugins on {side}",
            plotter=lambda df: px.scatter(df, x="year", y='lifeExp', title=f'Test plugins on side {side}'),
            plot_inputs={},
            data_source=self.df,
            plugins=[
                plg.DataFilterRadioButtons(
                    header="Filter country",
                    data_col="country",
                    data_values=["Canada", "United States", "Mexico"]
                )
            ],
            plugin_align=side
        )
        return plot_panel