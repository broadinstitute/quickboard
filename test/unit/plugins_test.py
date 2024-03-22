import plotly.express as px

import quickboard.base as qbb
import quickboard.plugins as plg
from test import TestTemplate


class PluginsTest(TestTemplate):
    """
    Tests:
        - All plugins for PlotPanels in two categories: discrete (e.g. RadioButtons) and continuous (e.g. Sliders)
        - Quickboard with tabs
        - PlotPanels with varying amounts of plots per tab
    """

    def make_test_board(self):
        # Set up tab for discrete plugins
        discrete_plugins_dict = {}
        for p in [
            self.make_radio_plugins(),
            self.make_dropdown_plugins(),
            self.make_checklist_plugins(),
        ]:
            discrete_plugins_dict.update(p)

        discrete_content_list = []
        for k, v in discrete_plugins_dict.items():
            discrete_content_list += [self.make_test_panel_discrete(plugins=v, plugin_group_name=k)]

        discrete_content_grid = qbb.ContentGrid(content_list=discrete_content_list)

        discrete_plugins_tab = qbb.BaseTab(
            tab_label="Discrete Plugins",
            tab_header="Discrete Plugins Test",
            content_list=[discrete_content_grid],
            # sidebar_header="Discrete Plugins Test",
            # sidebar_plugins=[]
        )

        # Set up tab for continuous plugins
        continuous_plugins_dict = {}
        for p in [
            self.make_slider_plugins(),
            self.make_range_slider_plugins()
        ]:
            continuous_plugins_dict.update(p)

        continuous_content_list = []
        for k, v in continuous_plugins_dict.items():
            continuous_content_list += [self.make_test_panel_continuous(plugins=v, plugin_group_name=k)]

        continuous_content_grid = qbb.ContentGrid(content_list=continuous_content_list)

        continuous_plugins_tab = qbb.BaseTab(
            tab_label="Continuous Plugins",
            tab_header="Continuous Plugins Test",
            content_list=[continuous_content_grid],
            # sidebar_header="Continuous Plugins Test",
            # sidebar_plugins=[]
        )

        return qbb.Quickboard(
            tab_list=[
                discrete_plugins_tab,
                continuous_plugins_tab
            ]
        )

    def make_radio_plugins(self):
        data_filter_radio = plg.DataFilterRadioButtons(
            header="Data Filter Radio Test",
            data_col='country',
            data_values=['Canada', 'United States', 'Mexico']
        )

        plot_input_radio = plg.PlotInputRadioButtons(
            header="Plot Input Radio Test",
            plot_input='y',
            data_values=['lifeExp', 'pop', 'gdpPercap']
        )

        return {'Radio Buttons': [data_filter_radio, plot_input_radio]}

    def make_dropdown_plugins(self):
        data_filter_dropdown = plg.DataFilterDropdown(
            header="Data Filter Dropdown Test",
            data_col='country',
            data_values=['Canada', 'United States', 'Mexico']
        )

        plot_input_dropdown = plg.PlotInputDropdown(
            header="Plot Input Dropdown Test",
            plot_input='y',
            data_values=['lifeExp', 'pop', 'gdpPercap']
        )

        return {'Dropdown': [data_filter_dropdown, plot_input_dropdown]}

    def make_checklist_plugins(self):
        data_filter_checklist = plg.DataFilterChecklist(
            header="Data Filter Checklist Test",
            data_col='country',
            data_values=['Canada', 'United States', 'Mexico']
        )

        return {'Checklist': [data_filter_checklist]}

    def make_slider_plugins(self):
        data_filter_slider = plg.DataFilterSlider(
            header="Data Filter Slider Test",
            data_col='pop',
            slider_min=int(self.df['pop'].min()),
            slider_max=int(self.df['pop'].max()),
            slider_default_value=int(self.df['pop'].min())
        )

        plot_input_slider = plg.PlotInputSlider(
            header="Plot Input Slider Test",
            plot_input='min_pop',
            slider_min=int(self.df['pop'].min()),
            slider_max=int(self.df['pop'].max()),
            slider_default_value=int(self.df['pop'].min())
        )

        return {'Slider': [data_filter_slider, plot_input_slider]}

    def make_range_slider_plugins(self):
        data_filter_range_slider = plg.DataFilterRangeSlider(
            header="Data Filter Range Slider Test",
            data_col='pop',
            slider_min=int(self.df['pop'].min()),
            slider_max=int(self.df['pop'].max())
        )

        plot_input_range_slider = plg.PlotInputRangeSlider(
            header="Plot Input Range Slider Test",
            plot_input='min_pop',
            slider_min=int(self.df['pop'].min()),
            slider_max=int(self.df['pop'].max())
        )

        return {'Range Slider': [data_filter_range_slider, plot_input_range_slider]}

    def make_test_panel_discrete(self, plugins, plugin_group_name):
        plot_panel = qbb.PlotPanel(
            header=f"Test for {plugin_group_name}",
            plotter=lambda df, y: px.scatter(df, x="year", y=y, title=f'Test filter discrete for {plugin_group_name}'),
            plot_inputs={
                'y': 'lifeExp',
            },
            data_source=self.df,
            plugins=plugins
        )
        return plot_panel

    def make_test_panel_continuous(self, plugins, plugin_group_name):
        def test_panel_continuous_plotter(df, min_pop=int(self.df['pop'].min())):
            # Handle Slider and RangeSlider uniformly
            if isinstance(min_pop, list):
                max_pop = min_pop[1]
                min_pop = min_pop[0]
            else:
                max_pop = int(df['pop'].max())
            sub_df = df[(df['pop'] <= max_pop) & (df['pop'] >= min_pop)]
            return px.scatter(sub_df, x="year", y='pop', title=f'Test filter discrete for {plugin_group_name}')

        plot_panel = qbb.PlotPanel(
            header=f"Test for {plugin_group_name}",
            plotter=test_panel_continuous_plotter,
            plot_inputs={},
            data_source=self.df,
            plugins=plugins
        )
        return plot_panel
