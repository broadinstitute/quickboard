import pandas as pd


class DataManager:
    """
    A class for interpreting different data sources, and cleaning data into a Pandas Dataframe for use
    by DynamicPanel objects. The possible types of data_source are:
        - pandas DataFrame (loaded in memory)
        - file path ending in .csv or .tsv (to be loaded into a DataFrame)
        - a list with first element a PlotPanel and second element a string with value either hoverData, clickData, or
        selectedData to be used for data generated from interacting with given PlotPanel.
    """
    def __init__(self, data_source=""):
        self.data_source = data_source
        self.source_type = None
        self.df = pd.DataFrame()

        if isinstance(data_source, pd.DataFrame):
            self.source_type = "DataFrame"

        elif isinstance(data_source, str):
            extension = data_source.split('.')[-1]
            if extension == 'tsv':
                self.source_type = "tsv"
            elif extension == 'csv':
                self.source_type = "csv"
            else:
                self.source_type = "tab"  # All other strings interpreted as use tab data

        elif isinstance(data_source, list):
            # Must have first entry a PlotPanel, and second entry string (one of: hoverData, clickData, selectedData)
            self.source_type = "PlotPanel"

        else:
            raise ValueError("Invalid data_source input. Please see documentation for list of valid input types.")

    def load_data(self):
        """
        Loads data into df attribute depending on type.
        """
        if self.source_type == "DataFrame":
            self.df = self.data_source

        elif self.source_type == "tsv":
            self.df = pd.read_csv(self.data_source, sep='\t')

        elif self.source_type == "csv":
            self.df = pd.read_csv(self.data_source)

        elif self.source_type == "PlotPanel":
            # Init as empty df w/ same cols
            self.df = pd.DataFrame({}, columns=self.data_source[0].data_manager.df.columns)

        else:
            self.df = pd.DataFrame()

    def get_interactive_indices(self, data):
        """
        Get list of indices of data chosen through interaction with plot.
        """
        if data != None:
            points = data["points"]
            index_list = []
            for p in points:
                index_list += p["customdata"]
            return index_list
        else:
            return []
