from sqlalchemy import create_engine
import pandas as pd

def get_data():
    '''
    OUTPUT:
    x_df: airline dataframes created by extracting data from corresponding airline table in psql database
    dfs: list of all dataframes available for analysis 
    '''
    engine = create_engine('postgresql://manuelcollazo:manuelcollazo@localhost:5432/airlines')

    southwest_df = pd.read_sql('SELECT * FROM southwest;',engine)
    american_df = pd.read_sql('SELECT * FROM american;',engine)
    delta_df = pd.read_sql('SELECT * FROM delta;',engine)
    united_df = pd.read_sql('SELECT * FROM united;',engine)

    ana_df = pd.read_sql('SELECT * FROM ana;',engine)
    japan_df = pd.read_sql('SELECT * FROM japan;',engine)

    qatar_df = pd.read_sql('SELECT * FROM qatar;',engine)

    dfs = [southwest_df,american_df,delta_df,united_df,ana_df,japan_df,qatar_df]

    for df in dfs:
        df['words'] = df['headline'] + df['body']
        df['positive'] = df['rating']>5
        df['positive'] = df['positive'].apply(lambda x: 1 if x == True else 0)

    return southwest_df,american_df,delta_df,united_df,ana_df,japan_df,qatar_df,dfs
