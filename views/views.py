# View (Dashboard layout)

def generate_table():
    ''' 
    Given a dataframe, return a table using dash components
    '''
    return

def on_load_division_options():
    '''
    Actions to perform on page load
    '''
    return

# Set up dashboard and create layout



import numpy as np


app = dash.Dash(

)
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

app.layout = html.Div(
    [
        html.H1(children='My Budget :^)'),

        dcc.Graph(
            id='weekly_spend',
            figure=go.Figure(
                data = [
                    go.Scatter(
                        x = ['1-Oct', '8-Oct', '15-Oct', '22-Oct', '29-Oct'],
                        y = [65, 68, 52, 60, 72],
                        name = 'All'
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