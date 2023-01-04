import dash_design_kit as ddk
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
import numpy as np
import pandas as pd
from app import app
import time
from numerize import numerize


dash.register_page(__name__, path='/')

# def inflate_col(data, col='trade_usd'):
#     """
#     Adjust a column for inflation
#     """
#     return data.apply(lambda x: cpi.inflate(x[col],
#                       x.year), axis=1) 
def convert(val):
    """
    Define the data types to use less memory and speed up the app
    """
    if val == np.nan:
        return 0
    return val 
start_t = time.time()
# df = pd.read_csv("data/commodity_trade_statistics_data.csv",low_memory=False, 
df = pd.read_csv("data/commodity_trade_statistics_data_adjusted.csv",low_memory=False, 
                 usecols=['country_or_area', 'year', 'commodity', 'flow', 'trade_usd', 'weight_kg'],
                 dtype={'trade_usd': np.float64, 'weight_kg': np.float64, 'year': np.int32, 'country_or_area': str, 'commodity': str, 'flow': str},nrows=1000000)
#converters={'trade_usd': convert, 'weight_kg': convert},
end_t = time.time()
print(f"Time to read csv: {end_t-start_t}")
print(f"Memory usage: {df.memory_usage().sum() / 1024**2} MB")
all_countries = df['country_or_area'].unique()

layout = ddk.App(
    [
        ddk.Header(
            [
                ddk.Logo(src=app.get_asset_url('earth.jpg')),
                ddk.Title("Flow & Commodity Breakdown",),
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            children=[
                                html.Label('Area', style={
                                    'fontSize': 30, 'textAlign': 'center'}),
                                dcc.Dropdown(
                                    id='country',
                                    options=[
                                        {"label": i, "value": i} for i in all_countries
                                    ],
                                    multi=False, 
                                    value='China',
                                    clearable=True,
                                    searchable=True,
                                ),
                                html.Div(id="Year-dropdown"),
                                html.Label('Year', style={
                                    'fontSize': 30, 'textAlign': 'center'},
                                           id = 'year_label'),
                                # Input2: 'year'
                                dcc.RangeSlider(
									id='year',
                                    marks={i: '{}'.format(i) for i in range(1980, 2020, 2)},
                                    dots=False,
									step=3,
         						),
                            ]
                        )
                    ),
                    width=8,
                ),
                ddk.Card(
                        width=24,
                        children=[
                            # TODO: Fit the number inside the card
                                ddk.CardHeader(title='Total traded across the selected years'),
                                ddk.DataCard(value=None, label='Total traded', id='display-total',
                                             style={'width':'fit-content',# fit the number inside the card
                                                    'fontSize': #inherit
                                                    '0.85vw',# align horizontally
                                                    }),
                        ],
                        # style={ 'margin': 'auto'},
                ),
                ddk.Card(
                    # width=56,
                    width=43,
                    children=[
                        ddk.CardHeader(
                            title=f'Import Export Breakdown'),
                        dcc.RadioItems(
                            ['Evolution', 'All Years'], value='Evolution', id='display-type', labelStyle={'display': 'inline-block', }),
                        dcc.Graph(id='display-flow', figure={}),

                    ],
                ),

                ddk.Card(
                    # width=43,
                    width=56,
                    children=[
                        ddk.CardHeader(title='Top 15 Commodities'),
                        dcc.RadioItems(['Bar', 'Pie'], value='Bar', id='chart-type', labelStyle={
                            'display': 'inline-block', }),
                        dcc.Graph(id='display-pie', figure={}, ),#center it
                    ],
                ),
            ],
        ),

    ]
),

# @app.callback(
#     [Output]
# )
# def set_datacard_value():
#     return 2   
@app.callback(
    [Output('year', 'min'),
    Output('year', 'max'),],
    [Input('country', 'value')],
)
def set_year_options(chosen_country):

    dff = df[df['country_or_area'] == (chosen_country)]
    min_year = dff['year'].min()
    max_year = dff['year'].max()
    return [min_year, max_year]

@app.callback(
    	Output('year', 'value'),
		[Input('year', 'min'),
		Input('year', 'max'),],
)
def set_type_value(start_year, year_end):
	return [start_year, year_end]


@app.callback(
    [
     Output('display-flow', 'figure'),
     Output('display-pie', 'figure'),
     Output('display-total', 'value')
     ],
    Input('country', 'value'),
    Input('year', 'value'),
    Input('chart-type', 'value'),
    Input('display-type', 'value'),
)
def update_graphs(selected_country,selected_year, chart_type, selected_type):
    if len(selected_country) == 0:
        return dash.no_update
    else:
        selected_year = list(range(selected_year[0], selected_year[1]+1))
        country_df = df[(df.country_or_area == (selected_country)) & (df.year.isin(selected_year))]

        # Export & Import comparison (Chart 1&2)
        if selected_type == 'Evolution':
            flow_breakdown = country_df.groupby(['country_or_area', 'year','flow'])['trade_usd'].sum().reset_index()
            fig_flow = px.line(flow_breakdown, x="year", y="trade_usd", color='flow',  hover_name="country_or_area",  render_mode="svg",)
            fig_flow.update_layout(legend_title='Flow Type',yaxis_title='Total Trade (USD)', xaxis_title='Year', )
            # add dollar sign to y axis
        else:
            # Total
            flow_breakdown = country_df.groupby(['country_or_area', 'flow'])['trade_usd'].sum().reset_index()
            fig_flow = px.bar(flow_breakdown, x='flow', y='trade_usd', color='flow', title=None,)
            fig_flow.update_layout(xaxis_title='Flow Type', yaxis_title='Total Trade (USD)', legend_title='Flow Type',)
        fig_flow.update_yaxes(tickprefix="$", )
        total_traded = flow_breakdown.trade_usd.sum()
            
        # Top 10 Commodities for selected country (and year) (Charts 2 & 3)
        df_commodity = pd.concat(
            [country_df['commodity'].str.split(', ', expand=True)], axis=1)
        # df_commodity=pd.concat([country_df['commodity'].str.split(', ', expand=True)], axis=1)
        top_commodities = df_commodity[0].value_counts().head(15)
        commodity_list = list(top_commodities.index)
        if chart_type == 'Pie':
            fig_commodities = px.pie(
                top_commodities, values=top_commodities.values, names=commodity_list, title=None)
            fig_commodities.update_layout(legend_title='Commodities') 
        else:
            fig_commodities = px.bar(
                top_commodities, x=list(top_commodities.index), y=top_commodities.values, color=top_commodities.index, title=None,labels=None)
            fig_commodities.update_layout(xaxis_title=None, yaxis_title='Frequency',legend_title='Commodities' )
    format_total = '${:,.0f}'.format(round(total_traded, 1))# ' USD'
    
    # format_total = numerize.numerize(total_traded,) + '$'
    return [fig_flow,fig_commodities,format_total]

if __name__ == "__main__":
    app.run_server(debug=True, port = 8050)

