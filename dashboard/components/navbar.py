# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc


# The navigation bar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/home")),
                dbc.NavItem(dbc.NavLink("Exports", href="/page1")),
            ],
            brand="Global Trade Dashboard",
            color="dark",
            dark=True,
        ),
    ])

    return layout
