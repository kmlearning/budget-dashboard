# Models
    # Total by timestamp
    # Total by timestamp by category
    # Total by category for time period
    # Count of values for category (for histogram)
    # Uncategorised transactions (table)
import pandas as pd
from sql_connection import get_database


connection = get_database()


def fetch_query(query):
    '''
    Runs a query against the sql db and returns the result as a pandas df
    '''
    df = pd.read_sql(query, con=connection)
    return df


def get_totals_by_time():
    '''
    Fetches time series of spending for all categories
    
    Arguments:
        category: String of the category to filter by, if any, e.g. "Groceries"

    Returns:
        Pandas dataframe of the time series of spending, for example:

            date    |   value
        -------------------------
         2018-01-01 |   31.00
         2018-01-02 |   15.00
    '''
    query = '''
        SELECT
            transdate,
            truecategory AS category, 
            SUM(value)
        FROM
            budget
        WHERE
            direction = 'out'
        GROUP BY
            transdate,
            truecategory
        '''
    spending_by_category = fetch_query(query)
    return spending_by_category

def get_total_spend():
    '''
    Fetches time series of total spending per day

    Returns:
        Pandas dataframe of the time series of spending, for example:

            date    |   value
        -------------------------
         2018-01-01 |   31.00
         2018-01-02 |   15.00
    '''
    query = '''
        SELECT
            transdate AS date,
            SUM(value) AS total
        FROM
            budget.transactions
        WHERE
            direction = 'out'
        GROUP BY
            transdate
        '''
    total_spending = fetch_query(query)
    return total_spending

def get_all_spend():
    '''
    Fetches time series of all spending transactions

    Returns:
        Pandas dataframe of the time series of spending, for example:

            date    |   value  |  description 
        --------------------------------------
         2018-01-01 |   31.00  | Shell Petrol
         2018-01-02 |   15.00  | McDonalds
    '''
    query = '''
        SELECT
            transdate AS date,
            value AS total,
            description
        FROM
            budget.transactions
        WHERE
            direction = 'out'
        '''
    all_out = fetch_query(query)
    return all_out