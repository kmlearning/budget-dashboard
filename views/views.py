import plotly.graph_objs as go
from models import models


def draw_category_time_series(dates, values):
    '''
    Create time series bar plot for weekly spending

    Arguments:
        dates: list of datetime values for beginning of week
        values: list of float values for total spending for week

    Returns:
        dictionary containing:
            data: 
                list of dictionary of x, y , name and type values
            layout:
                dictionary of plot title
    '''
    figure={
        'data': [
            {
                'x': dates,
                'y': values,
                'name': 'All',
                'type': 'bar'
            }
        ],
        'layout': {
            'title': 'Spend over time for category'
        }
    }
    return figure

def draw_spend_by_category_bar(totals, categories):
    ''' 
    Create bar plot layout, populate with input data and return 

    Arguments:
        totals: list of spending totals for each category
        categories: list of categories

    Returns:
        figure:
            a dictionary containing:
                data:
                    list of dictionary x, y, type, and name values
                layout:
                    dictionary of plot title
    '''
    figure={
        'data': [
            {
                'x': totals,
                'y': categories,
                'type': 'bar',
                'name': 'All',
                'orientation': 'h'
            }
        ],
        'layout': {
            'title': 'Spend by category'
        }
    }
    return figure

def draw_spend_for_category_hist(weekly_totals):
    '''
    Create Dash figure for histogram of spending for each week for category

    Arguments:
        weekly_totals
            list of total spending for each week for the category

    Returns:
        Dash figure graph object for histogram
    '''
    figure=go.Figure(
        data = [
            go.Histogram(
                x = weekly_totals,
                name = 'All',
                xbins = dict(
                    size= 'M2'
                ),
                autobinx = False
            )
        ],
        layout = go.Layout(
            title = 'Category Spend Histogram'
        )
    )
    return figure