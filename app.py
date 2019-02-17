import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go

from models import models
from views import views


app = dash.Dash()

all_spend = models.get_all_spend()
all_dates = all_spend['date']
all_totals = all_spend['total']
all_descriptions = all_spend['description']
all_category = all_spend['category']

weekly_spend = models.get_weekly_spend_by()
weekly_dates = weekly_spend['week']
weekly_totals = weekly_spend['total']


# REDO
month_year_options = models.month_year_options()
year_options = [{'label': year, 'value': year} for year in list(month_year_options.keys())]
#year_options = list(month_year_options)


app.layout = html.Div(
    [
        # Header
        html.H3(children='My Budget :^)'),

        # Category dropdown
        html.Div([
            html.Div('Select Category'),
            html.Div(
                dcc.Dropdown(
                    id='category-selector',
                    options=models.category_options()
                )
            )
        ]),

        # Time series
        dcc.Graph(
            id='spending-time-series'
        ),

        # Drop down selection
        html.Div([
            # Year dropdown
            html.Div([
                html.Div(
                    dcc.Dropdown(
                        id='year-selector',
                        options=year_options
                    ),
                    className='one column'
                )
            ]),
            # Month dropdown
            html.Div([
                html.Div(
                    dcc.Dropdown(
                        id='month-selector'
                    ),
                    className = 'one column'
                )
            ])
        ], className = 'row'),

        html.Div([
            # Bar chart spending by category
            html.Div(
                dcc.Graph(
                    id='bar-spend-categories'
                ),
                className = 'six columns'
            ),
            # Histogram category spending vs other periods
            html.Div(
                dcc.Graph(
                    id='hist-spend-categories'
                ),
                className = 'six columns'
            )
        ], className = 'row'
        )
    ]
)


@app.callback(
    Output(component_id='spending-time-series', component_property='figure'),
    [
        Input(component_id='category-selector', component_property='value')
    ]
)
def load_weekly_spend_time_series(category):
    ''' '''
    weekly_spend = models.get_weekly_totals_for_category(category)
    values = weekly_spend['week_total']
    dates = weekly_spend['week_start']

    figure = []
    if not values.empty:
        figure = views.draw_category_time_series(dates, values)
    return figure


@app.callback(
    Output(component_id='month-selector', component_property='options'),
    [
        Input(component_id='year-selector', component_property='value')
    ]
)
def populate_months(year):
    # something wrong here - works but flags error
    months = [{'label': month, 'value': month} for month in month_year_options[year]]
    #months = month_year_options[year]
    return months

@app.callback(
    Output(component_id='bar-spend-categories', component_property='figure'),
    [
        Input(component_id='year-selector', component_property='value'),
        Input(component_id='month-selector', component_property='value')
    ]
)
def load_spend_by_category(year, month):
    ''' Load data for spending by category bar chart into plot and return '''
    category_spend = models.get_spend_by_category(year, month)
    categories = category_spend['category']
    totals = category_spend['total']

    figure = []
    if not totals.empty:
        figure = views.draw_spend_by_category_bar(totals, categories)
    
    return figure

@app.callback(
    Output(component_id='hist-spend-categories', component_property='figure'),
    [
        Input(component_id='bar-spend-categories', component_property='clickData')
    ]
)
def load_spend_category_hist(clickData):
    '''
    Load data for spending each week for category histogram into plot and return
    '''
    category = clickData['points'][0]['y']
    weekly_totals = models.get_weekly_totals_for_category(category)
    weekly_totals = weekly_totals['week_total']

    figure = []
    if not weekly_totals.empty:
        figure = views.draw_spend_for_category_hist(weekly_totals)

    return figure

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


if __name__ == '__main__':
    app.run_server(
        #debug=True,
        #host='0.0.0.0',
        #port=8050
    )