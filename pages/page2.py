import dash_design_kit as ddk
# import pandas as pd
from numerize import numerize
import dash
from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from pages.home import df
from pages.page1 import get_top_countries_usd,find_earliest_year_with_value,find_latest_year_with_value,START_YEAR,END_YEAR

dash.register_page(__name__, path='/')

df_import = df[ (df['flow'] == 'Import') | (df['flow'] == 'Re-Import')]

# Main layout
layout = ddk.App(
    [
        ddk.Header(
            [
                ddk.Logo(src=app.get_asset_url('earth.jpg')),
                ddk.Title("Total Trade Analysis",),
                dcc.RadioItems(
                                    id="radio-chart-table", inline=True,
                                    value="Table",
                                    # style={'textAlign': 'center', 'width': '100%'},
                                    options=[
                                        {
                                            "label": html.Div(
                                                [
                                                    html.Img(
                                                        src="/assets/table.png", height=30),
                                                    html.Div("Table", style={
                                                        'font-size': 15, 'padding-left': 10}),
                                                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                                            ),
                                            "value": "Table"},
                                        {
                                            "label": html.Div(
                                                [
                                                    html.Img(
                                                        src="/assets/chart.png", height=30),
                                                    html.Div("Line", style={
                                                        'font-size': 15, 'padding-left': 10}),
                                                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                                            ),
                                            "value": "Line"},
                                        {
                                            "label": html.Div(
                                                [
                                                    html.Img(
                                                        src="/assets/earth.png", height=30),
                                                    html.Div("Choropleth", style={
                                                        'font-size': 15, 'padding-left': 10}),
                                                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                                            ),
                                            "value": "Choropleth"},
                                    ]),
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            children=[
                                html.Div(
                                    [
                                    html.H3('Value of imported of goods and services',id='page-title'),
                                    #'textAlign': 'center'}, id='page-title'),
                                    # 'fontSize': 30, 'textAlign': 'center'}, ),
                                    html.Small(  'Imports of goods and services represent the value of all goods and other market services received from the rest of the world.\
                                                  Data is adjusted for inflation and shown in constant U.S. dollars.\
                                                  The data is based on the 2017 revision of the United Nations Commodity Trade Statistics Database (UN COMTRADE).',)
                                    ],
                                    style={'textAlign': 'left', 'width': '80%'},
                                ),

                                html.Div(id="update-table2"),
                                html.Div(id="slider-container2", children=[
                                    dcc.RangeSlider(
                                        id="year-slider",
                                        step=1,
                                        marks={START_YEAR: f'{START_YEAR}',
                                               END_YEAR: f'{END_YEAR}'},
                                        value=[START_YEAR, END_YEAR],
                                        allowCross=True,
                                    )]),
                            ]

                        )
                    ),
                    width=12,),
            ],
        ),

    ]
),

# Call back to update table


########
@app.callback(
    Output('slider-container2', 'hidden'),
    [Input('radio-chart-table', 'value')],
)
def set_year_options(selected_chart):
    if selected_chart == 'Choropleth':
        return True
    return False

@app.callback(
    Output("update-table2", "children"),
    [Input("year-slider", "value"),
     Input("radio-chart-table", "value")
     ],
)
def update_output(selected_years, chart_type):
    start_year = str(selected_years[0])
    end_year = str(selected_years[1])

    # select data in range
    selected_range = list(range(int(start_year), int(end_year)+1))
    dff_import = df_import[df_import['year'].isin(selected_range)]
    # absolute_change_table = absolute_change_table[['country_or_area',start_year,end_year,'change','earliest_year_available']]

    graph = 1
    if chart_type == 'Table':
        # Table: (Chart 1)
        global_import_pivot = dff_import.pivot_table(
            index='country_or_area', columns='year', values='trade_usd', aggfunc='sum').reset_index()
        earliest_year_available = global_import_pivot.apply(
            lambda x: find_earliest_year_with_value(x, START_YEAR, END_YEAR), axis=1)
        latest_year_available = global_import_pivot.apply(
            lambda x: find_latest_year_with_value(x, START_YEAR, END_YEAR), axis=1)
        global_import_pivot.columns = global_import_pivot.columns.astype(str)
        # Now we can fill the missing values with the closest available year (from the right)
        global_import_pivot = global_import_pivot.fillna(
            method='bfill', axis=1)
        # Fill the missing values with the closest available year (from the left)
        global_import_pivot = global_import_pivot.fillna(
            method='ffill', axis=1)
        absolute_change_table = global_import_pivot[[
            'country_or_area', start_year, end_year]]
        absolute_change_table['Absolute Change'] = absolute_change_table[end_year] - \
            absolute_change_table[start_year]
        absolute_change_table['earliest_year_available'] = earliest_year_available
        absolute_change_table['latest_year_available'] = latest_year_available
        absolute_change_table = absolute_change_table.sort_values(
            by=['Absolute Change'], ascending=False)
        absolute_change_table = absolute_change_table.rename(
            columns={'country_or_area': 'Country'})
        # Format the table
        absolute_change_table[start_year] = absolute_change_table[start_year].apply(
            lambda x: "${:,}".format(round(x)))
        absolute_change_table[end_year] = absolute_change_table[end_year].apply(
            lambda x: "${:,}".format(round(x)))
        absolute_change_table['Absolute Change'] = absolute_change_table['Absolute Change'].apply(
            lambda x: "${:,}".format(round(x)))
        
        graph = html.Div(
            [
                dash_table.DataTable(
                    absolute_change_table.to_dict('records'),
                    columns=[{'name': str(i), 'id': str(i)}
                             for i in absolute_change_table.columns],
                    id='tbl', style_cell={'textAlign': 'left'},
                    style_header={
                        'backgroundColor': '#075264',
                        'fontWeight': 'bold',
                        'textDecoration': 'none',
                        'color': 'white',
                    },
                    # page_size=10,
                    style_table={'height': '550px', 'overflowY': 'auto'},
                    css=[{"selector": ".show-hide", "rule": "display: none"}],
                    hidden_columns=['earliest_year_available',
                                    'latest_year_available'],
                    # Hover info
                    tooltip_data=[
                        {
                            # show tooltip if the value is not the same as the value in the earliest_year_available(latest_year_available) column
                            f'{start_year}': {'value': f'Showing closest available data point {row["earliest_year_available"]}'
                                              if str(row["earliest_year_available"]) != start_year else '',
                                              'type': 'markdown',
                                              },
                            f'{end_year}': {'value': f'Showing closest available data point {row["latest_year_available"]}'
                                            if str(row["latest_year_available"]) != end_year else '', 
                                            'type': 'markdown',
                                            },
                        } for row in absolute_change_table.to_dict('records') 
                    ],
                    style_cell_conditional=[
                        {
                            'if': {
                                'filter_query': '{{earliest_year_available}} > {}'.format((start_year)),
                                'column_id': start_year,
                            },
                            'color': 'lightgrey',
                            'onhover': 'tooltip'
                        },
                        {
                            'if': {
                                'filter_query': '{{latest_year_available}} < {}'.format((end_year)),
                                'column_id': end_year,
                            },
                            'color': 'lightgrey',
                            # 'textDecoration': 'underline',
                            'onhover': 'tooltip'
                        }
                    ],
                ),
            ])
    elif chart_type == 'Line':
        # Chart 2
        df_flow = dff_import
        # Select top 10 countries (by import) for line chart
        df_flow_top = get_top_countries_usd(df_flow, top=15)
        top_10_flow_table = df_flow_top.groupby(
            ['year', 'country_or_area'], as_index=False)[['trade_usd']].sum()
        top_10_flow_table.sort_values(by=['year'], inplace=True)
        top_10_flow_table.reset_index(inplace=True)
        top_10_flow_chart = px.line(top_10_flow_table, x='year', y='trade_usd', color='country_or_area',
                                    title=None, labels={'trade_usd': 'Value of Imported goods in USD', 'year': 'Year', 'country_or_area': 'Top 15 Areas'}, height=550)
        top_10_flow_chart.update_yaxes( tickprefix="$")

        graph = html.Div([
            dcc.Graph(
                id='line_chart',
                figure=top_10_flow_chart
            )
        ])
    else:
        # Choropleth (Chart 3)
        global_import_table = dff_import.groupby(['year', 'country_or_area'], as_index=False)[
            ['trade_usd']].sum()
        choropleth_fig = px.choropleth(global_import_table, locations="country_or_area", color="trade_usd", hover_name="country_or_area",
                                       animation_frame="year", color_continuous_scale=px.colors.sequential.Reds, locationmode='country names',
                                       scope='world', title=None, labels={'trade_usd': 'Value of Imported goods in USD', 'year': 'Year'},
                                       range_color=[0, 500000000000], height=550)
        graph = html.Div([
            dcc.Graph(
                id='choropleth_chart',
                figure=choropleth_fig,
            )
        ])

    return graph
