import dash
import jupyter_dash
import dash_bootstrap_components as dbc
from quickboard.utils.environment import isnotebook


theme = dbc.themes.BOOTSTRAP
if isnotebook():
    # Initialize app
    # Other nice themes: DARKLY, CYBORG, BOOTSTRAP, FLATLY, LUX, LUMEN, SOLAR
    app = jupyter_dash.JupyterDash(external_stylesheets=[theme])
    app.config.suppress_callback_exceptions = True   # Ignore errors from other tab features not present on start tab
else:
    app = dash.Dash(external_stylesheets=[theme])
