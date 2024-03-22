import webbrowser

from plotly.data import gapminder
from quickboard.app import start_app


class TestTemplate:
    """
    A template for making test objects.
    """
    def __init__(self):
        self.df = gapminder()

    def make_test_board(self):
        # Method to produce Quickboard object for test; override in child class
        pass

    def run_test(self, port):
        test_name = type(self).__name__

        print(f"Starting app for test: {test_name}")
        start_app(self.make_test_board(), port=port, app_title=test_name)

        # print(f"Navigating web browser to port: {port}")
        # url = f"http://localhost:{port}/"
        # webbrowser.open_new(url)