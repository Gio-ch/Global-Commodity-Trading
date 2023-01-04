# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc


# The navigation bar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Breakdown", href="/home")),
                dbc.NavItem(dbc.NavLink("Export Evolution", href="/page1")),
                dbc.NavItem(dbc.NavLink("Import Evolution", href="/page2")),
            ],
            # brand="Global Trade Dashboard",
            color="dark",
            dark=True,
        ),
    ])

    return layout
