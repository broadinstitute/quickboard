import dash
import jupyter_dash
import dash_bootstrap_components as dbc
from quickboard.utils.environment import isnotebook


theme = dbc.themes.BOOTSTRAP
# Other nice themes: DARKLY, CYBORG, BOOTSTRAP, FLATLY, LUX, LUMEN, SOLAR

if isnotebook():
    # Initialize app
    app = jupyter_dash.JupyterDash(__name__, external_stylesheets=[theme])
    app.config.suppress_callback_exceptions = True   # Ignore errors from other tab features not present on start tab
else:
    app = dash.Dash(__name__, external_stylesheets=[theme])
