
# import plotly.graph_objs as go
import dash_design_kit as ddk
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
# from dash import dash_table
import plotly.express as px
import numpy as np
import pandas as pd
from app import app

dash.register_page(__name__, path='/')

# Data handling (cleaning, aggregating, etc.)
df = pd.read_csv("data/data.csv")
# df = pd.read_csv("data/commodity_trade_statistics_data.csv")

all_countries = df['country_or_area'].unique()
# all_years = df['year'].unique()

layout = ddk.App(
    [
        ddk.Header(
            [
                ddk.Logo(src=app.get_asset_url('earth.jpg')),
                ddk.Title("Global Commodity Trade Data",),
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            children=[
                                # Input1: 'country'
                                html.Label('Area', style={
                                    'fontSize': 30, 'textAlign': 'center'}),
                                dcc.Dropdown(
                                    # id='period',
                                    id='country',
                                    options=[
                                        {"label": i, "value": i} for i in all_countries
                                    ],
                                    multi=False,  # True
                                    # value= all_countries,
                                    value='China',
                                    clearable=True,
                                    searchable=True,
                                ),
                                html.Div(id="Year-dropdown"),
                                html.Label('Year', style={
                                    'fontSize': 30, 'textAlign': 'center'}),
                                # Input2: 'year'
                                dcc.RangeSlider(
									id='year',
                                    marks={i: '{}'.format(i) for i in range(1990, 2020, 2)},
                                    dots=False,
									step=5,
         						),

								# Original working code
                                # dcc.Dropdown(
                                #     		id='year',  
                                #       		multi=True,
                                #             options =[],
                                #             value=[]

                                # ),
                                # dcc.Dropdown(id='display-type', options=[], multi=True, value=commo_list[:2]),
                            ]
                        )
                    ),
                    # full width
                    width=12,
                    # width=8,
                ),

                # TODO
                # ddk.Card(
                # width=26,
                # # height=40,
                # children=[
                #         ddk.CardHeader(title='Top 10 Commodities by Trade Value'),
                #         # ddk.CardHeader(title='Total Fossils Found Across All Periods'),
                #         # ddk.DataCard(value=totalFossilsFounds,
                #         # a circle graph
                #         # ddk.DataCard(value=f'Top {total_category_count}',
                #         #         style={'width':'fit-content'}),
                #         # dcc.Graph(figure=fig),


                # ]
                # ),

                # ddk.Card(
                # width=24,
                # children=[
                #         ddk.CardHeader(title='Total Fossils Found'),
                #         ddk.DataCard(
                #                 id='total-fossils',
                #                 value='',
                #                 style={'width':'fit-content'}),
                # ]
                # ),

                # ddk.Card(
                # width=40,
                # children=[
                #         dcc.Graph(figure=px.scatter_geo(df2, lat='Latitude', lon='Longitude', color="Period", size='LatLongPeriodCount',
                #         hover_name="Country").update_geos(projection_type="orthographic")),
                # ],
                # ),
                ddk.Card(
                    # width=43,
                    width=56,
                    children=[
                        dcc.RadioItems(
                            ['Bar', 'Pie'], value='Bar', id='display-type', labelStyle={'display': 'inline-block', }),
                        ddk.CardHeader(
                            title=f'Which Country Fossils Were Found'),
                            # title='Which Country Fossils Were Found'),
                        # dcc.Graph(id='display-scatter', figure={}),
                        # ddk.Graph(id='display-bar', figure={}),
                        dcc.Graph(id='display-bar', figure={}),

                    ],),

                ddk.Card(
                    # width=56,
                    width=43,
                    children=[
                        # select bar or pie
                        dcc.RadioItems(['Import', 'Export', 'Both'], value='Import', id='flow', labelStyle={
                            'display': 'inline-block', }),
                        ddk.CardHeader(title='Top 10 Commodities'),
                        # dcc.Graph(figure=fig),
                        dcc.Graph(id='display-pie', figure={}),
                        # ddk.Graph(id='display-map', figure={}),
                    ],
                ),
            ],
        ),

    ]
),


@app.callback(
    # Output('year', 'options'),
    [Output('year', 'min'),
    Output('year', 'max'),],
    [Input('country', 'value')],
)
def set_year_options(chosen_country):

    dff = df[df['country_or_area'] == (chosen_country)]
    min_year = dff['year'].min()
    max_year = dff['year'].max()
    return [min_year, max_year]
    # sorted_years = sorted(dff['year'].unique())
    
    # df.drop_duplicates(subset='brand')
    # return [{'label': c, 'value': c} for c in sorted_years]

####### Original code
# @app.callback(
#     # Output('display-type', 'options'),
#     Output('year', 'options'),
#     #     [Input('period', 'value')],
#     [Input('country', 'value')],
#     # [Input('category', 'value')],
# )
# def set_year_options(chosen_country):

#     dff = df[df['country_or_area'] == (chosen_country)]
#     sorted_years = sorted(dff['year'].unique())
#     # df.drop_duplicates(subset='brand')
#     return [{'label': c, 'value': c} for c in sorted_years]
 

@app.callback(
    	Output('year', 'value'),
		[Input('year', 'min'),
		Input('year', 'max'),],
        # Input('year', 'options'),
        # Input('year', 'options'),
)
def set_type_value(year_start, year_end):
	return [year_start, year_end]


# @app.callback(
#         Output('year', 'value'),
#         Input('year', 'options'),
#         # [Input('country', 'value')]
# )
# def set_type_value(available_options):
# 	# return [x['value'] for x in available_options]
	
# 	# return available_options[0]['value']
# 	return [x['value'] for x in available_options]

@app.callback(
    [Output('display-bar', 'figure'),
     Output('display-pie', 'figure')],
    Input('country', 'value'),
    Input('year', 'value'),
    Input('flow', 'value'),
    Input('display-type', 'value'),
    # Input('period', 'value'),
)
# Output('total-fossils', 'children'),
# Input('display-type', 'value'),
# Input('period', 'value')
# def update_graph(selected_country):#, selected_period):
# selected_period):
def update_data(selected_country,selected_year, selected_flow, selected_type):
    if len(selected_country) == 0:
        return dash.no_update
    else:
        
        # df_country = df[(df.country_or_area == (selected_country)) & (df.year == (selected_year))]
        df_country = df[(df.country_or_area == (selected_country)) & (df.year.isin(selected_year))]
        if len(df_country) == 0:
            # display that no data is available
            pass
            # return dash.no_update

        # 1.
        # Export & Import comparison (Chart 1)
        df_flow = df_country['flow'].value_counts()
        if selected_type == 'Bar':
                fig_flow = px.bar(df_flow, x=df_flow.index, y=df_flow.values, color=df_flow.index, title=None,)
                # fig_flow.update_traces(showlegend=False)
        else:
                fig_flow = px.pie(df_flow, values=df_flow.values, names=df_flow.index, title=None,)

        # 2.
        # selected_flow
        if selected_flow == 'Import':
            df_commodity = df_country[(df_country['flow'] == 'Import') | (
                df_country['flow'] == 'Re-Import')]
        elif selected_flow == 'Export':
            df_commodity = df_country[(df_country['flow'] == 'Export') | (
                df_country['flow'] == 'Re-Export')]
        else:
            df_commodity = df_country

        # Top 10 Commodities for selected country (and year) (Charts 2 & 3)
        df_commodity = pd.concat(
            [df_commodity['commodity'].str.split(', ', expand=True)], axis=1)
        # df_commodity=pd.concat([df_country['commodity'].str.split(', ', expand=True)], axis=1)
        top_commodities = df_commodity[0].value_counts().head(10)
        commodity_list = list(top_commodities.index)
        fig_commodities = px.pie(
            top_commodities, values=top_commodities.values, names=commodity_list, title=None)

    return [fig_flow, fig_commodities]

    # return fig,fig2
# def update_cards(selected_period):
#         dff = df[(dff.Type.isin(selected_period))]
#         fig = ddk.Card(value='Name')
#         return fig


if __name__ == "__main__":
    app.run_server(debug=True, port = 8050)


# OLD
# dff = df[ df.commodity.str.contains('|'.join(selected_type)) ]
# table1 = dff.groupby(['country_or_area', 'commodity'], as_index=False)[['trade_usd']].sum().sort_values(by='trade_usd', ascending=False)

# table1 = dff.groupby(['country_or_area', 'category'], as_index=False)[['trade_usd']].sum().sort_values(by='trade_usd', ascending=False)
# fig1 = px.bar(table1, x='country_or_area', y='trade_usd', color='commodity',)
# fig2 = px.scatter_geo(df3, lat='Latitude', lon='Longitude', color="Period", size='LatLongTypeCount',
#         hover_name="Country").update_geos(projection_type="orthographic")

# fig = px.bar(dff.sample(50), x='Country', color= 'Period',)# size='MillionsYears')
