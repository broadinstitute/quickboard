from unit.plugins_test import PluginsTest
from unit.plotpanel_test import PlotPanelTest


STARTING_PORT = 8060
MAX_PORT = 8100

plugins_test = PluginsTest()
plotpanel_test = PlotPanelTest()

try:
    plugins_test.run_test(port=8060)
    # plotpanel_test.run_test(port=8060)
except:
    plugins_test.run_test(port=8061)
    # plotpanel_test.run_test(port=8061)
