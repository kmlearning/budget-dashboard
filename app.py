'''
# standard library
import os

# dash libs
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
import plotly.graph_objs as go

# pydata stack
import pandas as pd
from sqlalchemy import create_engine

# set params
conn = create_engine(os.environ['DB_URI'])


#############################################
# Interaction Between Components / Controller
#############################################

# Template
@app.callback(
    Output(component_id='selector-id', component_property='figure'),
    [
        Input(component_id='input-selector-id', component_property='value')
    ]
)
def ctrl_func(input_selection):
    return None


# start Flask server
if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='0.0.0.0',
        port=8050
)
'''


import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go

from models import models

app = dash.Dash()

all_spend = models.get_all_spend()
all_dates = all_spend['date']
all_totals = all_spend['total']
all_descriptions = all_spend['description']

weekly_spend = models.get_total_spend()
weekly_dates = weekly_spend['date']
weekly_totals = weekly_spend['total']

app.layout = html.Div(
    [
        html.H1(children='My Budget :^)'),
        dcc.Graph(
                id='all_trans',
                figure=go.Figure(
                    data = [
                        go.Scatter(
                            x = all_dates,
                            y = all_totals,
                            text = all_descriptions,
                            name = 'All',
                            mode='markers'
                        )
                    ],
                    layout = go.Layout(
                        title = 'All Transactions'
                    )
                )
            ),
            dcc.Graph(
                id='weekly_spend',
                figure=go.Figure(
                    data = [
                        go.Scatter(
                            x = weekly_dates,
                            y = weekly_totals,
                            name = 'Weekly',
                            mode='lines+markers'
                        )
                    ],
                    layout = go.Layout(
                        title = 'Total Weekly Spend'
                    )
                )
            ),
            dcc.Graph(
                id='by_category',
                figure={
                    'data': [
                        {
                            'x': [425, 200, 170, 160, 120],
                            'y': ['Rent', 'Groceries', 'Debt', 'Lunch'],
                            'type': 'bar',
                            'name': 'All',
                            'orientation': 'h'
                        }
                    ],
                    'layout': {
                        'title': 'Spend by category'
                    }
                }
            ),
            dcc.Graph(
                id='category_hist',
                figure=go.Figure(
                    data = [
                        go.Histogram(
                            x = np.random.randn(500),
                            name = 'All'
                        )
                    ],
                    layout = go.Layout(
                        title = 'Category Spend Histogram'
                )
            )
        )
    ]
)


if __name__ == '__main__':
    app.run_server()