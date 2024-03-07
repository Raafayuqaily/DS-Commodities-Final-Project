# This python file is designed to Preprocess the loaded data
# Preprocessing includes checking variable data types and sorting the data

import load_commodities_data
import config
from pathlib import Path
import pandas as pd

DATA_DIR = Path(config.DATA_DIR)

df = load_commodities_data.load_data(data_dir=DATA_DIR, file_name = "commodities_data.csv")

def preprocess_data(df):
    """
    Rename the price column to 'ClosePrice'
    Ensure Data types are as expected. For example, 'Date' must be a datetime object
    Sort Data
    """
    df_prep = df
    df_prep = df_prep.rename(columns = {'PX_LAST':'ClosePrice'})
    
    df_prep['Date'] = pd.to_datetime(df_prep['Date'])
    df_prep['Contract'] = df_prep['Contract'].astype(int)
    df_prep['ClosePrice'] = df_prep['ClosePrice'].astype(float)

    #Creating a column for YearMonth, which makes analysis easier
    df_prep['YearMonth'] = df_prep['Date'].dt.to_period('M')
    
    df_prep.sort_values(by=['Date','Commodity'], inplace = True)
    df_prep.set_index('Date', inplace = True)

    return df_prep

if __name__ == '_main_':
    preprocess_data(df)



