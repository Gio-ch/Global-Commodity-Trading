
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,
                # external_stylesheets=[dbc.themes.BOOTSTRAP],
                external_stylesheets=[dbc.themes.SOLAR],
                meta_tags=[{"name": "viewport",
                            "content": "width=device-width"}],
                suppress_callback_exceptions=True)
