import pandas as pd
from sql_connection import get_database


connection = get_database()


def fetch_query(query, params =None):
    '''
    Runs a query against the sql db and returns the result as a pandas df

    Arguments:
        query: 
            a single string containing the sql query to be run
        params: 
            a list of paramaters to be injected into the query in place of 
            ? symbols
    Returns:
        df:
            pandas dataframe with results of the query
    '''
    df = pd.read_sql(query, con=connection, params=params)
    return df

def category_options():
    query = '''
        SELECT
            category
        FROM
            budget.category_budgets
        '''
    categories = fetch_query(query)['category']
    categories = [{'label': category, 'value': category} for category in categories]
    return categories

def get_spend_for_category(category):
    ''' Get time series of all spending data for specific category '''
    query =  '''
        SELECT
            transdate AS date,
            value,
            description
        FROM
            budget.transactions
        WHERE
            direction = 'out'
            AND
            truecategory = %(category)s
        ORDER BY
            transdate DESC
    '''
    spend_for_category = fetch_query(query, params={'category': category})
    return spend_for_category

def get_weekly_totals_for_category(category):
    ''' Get weekly spending totals for a given category '''
    query =  '''
        SELECT
            SUM(value) AS week_total,
            week_start
        FROM (
            SELECT
                value,
                transdate,
                date_trunc('week', transdate) AS week_start
            FROM
                budget.transactions
            WHERE
                direction = 'out'
                AND
                truecategory = %(category)s
        ) t1
        GROUP BY
            week_start
    '''
    spend_for_category = fetch_query(query, params={'category': category})
    return spend_for_category

def get_monthly_totals_for_category(category):
    ''' Get monthly spending totals for a given category '''
    query = '''
        SELECT
            SUM(value) AS month_total,
            month,
            year
        FROM (
            SELECT
                value,
                transdate,
                extract(month from transdate) AS month
                extract(year from transdate) AS year
            FROM
                budget.transactions
            WHERE
                direction = 'out'
                AND
                truecategory = %(category)s
        ) t1
        GROUP BY
            month, 
            year
    '''
    spend_for_category = fetch_query(query, params={'category': category})
    return spend_for_category

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
        ORDER BY
            transdate
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
            truecategory AS category,
            description
        FROM
            budget.transactions
        WHERE
            direction = 'out'
        ORDER BY
            transdate
        '''
    all_out = fetch_query(query)
    return all_out

def get_weekly_spend_by(category = None):
    '''
    Fetches time series of weekly spend for given category
    '''
    if category:
        query = '''
            SELECT
                date_trunc('week', transdate::date) AS week,
                SUM(value) AS total
            FROM
                budget.transactions
            WHERE
                truecategory = ?
                AND
                direction = 'out'
            GROUP BY
                week
        '''
    else:
        query = '''
            SELECT
                date_trunc('week', transdate::date) AS week,
                SUM(value) AS total
            FROM
                budget.transactions
            WHERE
                direction = 'out'
            GROUP BY
                week
        '''
        weekly_spend = fetch_query(query)
        return weekly_spend


def get_spend_by_category(year, month):
    '''
    Fetch and return total spending by category as pandas df
    '''
    query = '''
        SELECT
            SUM(value) AS total,
            truecategory AS category
        FROM
            budget.transactions
        WHERE
            direction = 'out'
            AND
            extract(year from transdate) = %(year)s
            AND
            extract(month from transdate) = %(month)s
        GROUP BY
            truecategory
        ORDER BY
            total
    '''
    spend_by_category = fetch_query(query, params={'year':year, 'month': month})
    return spend_by_category 

def year_options():
    ''' Return list of available years '''
    query = '''
        SELECT
            DISTINCT extract(year from transdate) AS yr
        FROM
            budget.transactions
        ORDER BY
            extract(year from transdate) DESC
    '''
    years_df = fetch_query(query)
    years_list = list(years_df['yr'].astype('int32').values)
    return years_list

def all_month_options():
    ''' Return list of available months '''
    query = '''
        SELECT
            DISTINCT extract(month from transdate) AS mon
        FROM
            budget.transactions
        ORDER BY
            extract(month from transdate) DESC
    '''
    mon_df = fetch_query(query)
    mon_list = list(mon_df['mon'].astype('int32').values)
    return mon_list

def month_year_options():
    ''' 
    Get month-year options and return as nested json
    
    Returns:
        {
            year1: [
                mon1,
                mon2
            ],
            year2: [
                mon1
            ]
        }
    '''
    query = '''
        SELECT
            date_part('month', transdate) AS mon,
            date_part('year', transdate) AS yr
        FROM
            budget.transactions
        GROUP BY
            date_part('month', transdate),
            date_part('year', transdate)
        ORDER BY
            date_part('year', transdate) DESC,
            date_part('month', transdate) DESC
    '''
    df = fetch_query(query)
    month_years = {}
    for index, row in df.iterrows():
        year = int(row['yr'])
        month = int(row['mon'])
        if year not in month_years.keys():
            month_years[year] = []
        if month not in month_years[year]:
            month_years[year].append(month)
    return month_years